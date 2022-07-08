#!/usr/bin/env python3
"""
Seismic migration performs a 'time-reverse migration', or backprojection.
In the terminology of seismic imaging, we are running a forward and adjoint
simulation to derive the gradient of the objective function. This workflow
sets up the machinery to derive a scaled, smoothed gradient from an initial
model
"""
import os

from seisflows.workflow.forward import Forward
from seisflows.tools import msg
from seisflows.tools.specfem import Model


class Migration(Forward):
    """
    Migration base class.

    Performs the workflow of an inversion up to the postprocessing. In the
    terminology of seismic exploration, implements a 'reverse time migration'.
    """
    def __init__(self):
        """
        Init is used to instantiate global parameters defined by the input
        parameter file.
        """
        super().__init__()

        self.required.par(
            "CASE", required=False, default="data", par_type=str,
            docstr="How to address 'data' in your workflow, available options: "
                   "1) 'data': Real data inversion. Observed waveforms must be "
                   "provided by the user in PATH.DATA/{SOURCE_NAME}. OR if "
                   "PAR.PREPROCESS=='pyatoa' data should be discoverable "
                   "via IRIS webservices based on event ID and station codes"
                   "2) 'synthetic': A synthetic-synthetic workflow. 'Data' "
                   "will be generated as synthetics using PATH.MODEL_TRUE. "
        )
        self.required.par(
            "SAVEGRADIENT", required=False, default=True, par_type=bool,
            docstr="Save gradient files each time the gradient is evaluated"
        )
        self.required.par(
            "SAVEKERNELS", required=False, default=False, par_type=bool,
            docstr="Save event kernel files each time they are evaluated"
        )
        self.required.par(
            "SAVEAS", required=False, default="binary", par_type=str,
            docstr="Format to save models, gradients, kernels. Available: "
                   "['binary': save files in native SPECFEM .bin format, "
                   "'vector': save files as NumPy .npy files, "
                   "'both': save as both binary and vectors]"
        )
        self.required.path(
            "GRAD", required=False,
            default=os.path.join(self.path.WORKDIR, "scratch", "evalgrad"),
            docstr="scratch path to store any models or kernels related to "
                   "gradient evaluations. Sub-directories will be generated "
                   "inside PATH.GRAD to save various stages of gradient "
                   "manipulation"
        )
        self.required.path(
            "MODEL_TRUE", required=False,
            default=os.path.join(self.path.WORKDIR, "specfem", "MODEL_TRUE"),
            docstr="Target model to be used for PAR.CASE == 'synthetic'. The "
                   "TRUE model will be used to evaluate forward simulations "
                   "ONCE at the beginning of the workflow, to generate 'data'."
        )

    def check(self, validate=True):
        """
        Checks parameters and paths. Must be implemented by sub-class
        """
        super().check(validate=validate)

        if self.par.CASE.upper() == "SYNTHETIC":
            assert os.path.exists(self.path.MODEL_TRUE), \
                "CASE == SYNTHETIC requires PATH.MODEL_TRUE"

        if not self.path.DATA or not os.path.exists(self.path.DATA):
            assert "MODEL_TRUE" in self.path, f"DATA or MODEL_TRUE must exist"

    def setup(self, flow=None, return_flow=False):
        """
        Override the Forward.setup() method to include new flow functions
        AND run setup for a the Postprocess module which will be used to deal
        with the gradient
        """
        super().setup(flow=flow, return_flow=return_flow)

        postprocess = self.module("postprocess")
        postprocess.setup()

    def main(self, flow=None, return_flow=False):
        """Inherits from seisflows.workflow.forward.Forward"""
        flow = (self.evaluate_initial_misfit,
                self.evaluate_gradient,
                self.process_kernels,
                self.scale_gradient
                )

        self.main(flow=flow, return_flow=return_flow)

    def evaluate_initial_misfit(self):
        """Inherits from seisflows.workflow.forward.Forward"""
        super().evaluate_initial_misfit()

    def evaluate_gradient(self, path=None):
        """
        Performs adjoint simulation to retrieve the gradient of the objective.

        .. note::
            In the terminology of seismic exploration, we are 'backprojecting'
        """
        system = self.module("system")

        self.logger.info(msg.mnr("EVALUATING GRADIENT"))
        self.logger.debug(
            f"evaluating gradient {self.par.NTASK} times on system..."
        )
        system.run("solver", "eval_grad", path=path or self.path.GRAD,
                   export_traces=self.par.SAVETRACES)

    def process_kernels(self):
        """
        System-run wrapper for postprocess.process_kernels which is meant to
        sum and smooth all individual event kernels
        """
        system = self.module("system")
        self.logger.info(msg.mnr("PROCESSING KERNELS"))

        # Runs kernel processing as a single parallel process
        system.run("solver", "postprocess_kernels", single=True,
                   path_grad=self.path.GRAD)

    def scale_gradient(self):
        """
        Scale the gradient magnitude by the given model, write the gradient in
        vector form and model form, and apply an optional mask to the gradient

        .. note::
            While both masking and preconditioning involve scaling the
            gradient, they are fundamentally different operations:
            masking is ad hoc, preconditioning is a change of variables;
            For more info, see Modrak & Tromp 2016 GJI
        """
        model = Model(path=os.path.join(self.path.GRAD))
        gradient = Model(path=os.path.join(self.path.GRAD, "kernels", "sum"))

        # Merge to vector and convert to absolute perturbations:
        # log dm --> dm (see Eq.13 Tromp et al 2005)
        gradient.vector *= model.vector

        if self.path.MASK:
            mask = Model(os.path.join(self.path.MASK))
            # Write out a non-masked gradient incase masking is not wanted
            gradient.write(path=os.path.join(self.path.GRAD, "gradient_nomask"))

            gradient.vector *= mask.vector

        # Update the model values based on the vector manipulation
        gradient.model = gradient.split()

        # Write the gradient out
        gradient.write(path=os.path.join(self.path.GRAD, "gradient"))
        gradient.save(path=os.path.join(self.path.OPTIMIZE, "g_new"))


