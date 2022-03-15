"""
SeisFlows3 messages tool. For providing a uniform look to SeisFlows3 print
and log statements.
"""
from textwrap import wrap


def mjr(val):
    """
    Message formatter used to block off sections in log files with visually
    distinctive separators. Defined as individual functions to simplify
    calling and reduce code length.

    Major: For important or workflow.main() messages like starting workflow

    :type val: str
    :param val: formatted message to return
    :rtype: str
    :return: formatted string message to be printed to std out
    """
    mjr_ =  """
================================================================================
{:^80s}
================================================================================
"""

    return mjr_.format(val)


def mnr(val):
    """
    Message formatter used to block off sections in log files with visually
    distinctive separators. Defined as individual functions to simplify
    calling and reduce code length.

    Minor: For key messages, describing things like what iteration were at

    :type val: str
    :param val: formatted message to return
    :rtype: str
    :return: formatted string message to be printed to std out
    """
    mnr_ = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{:^80s}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

    return mnr_.format(val)


def sub(val):
    """
    Message formatter used to block off sections in log files with visually
    distinctive separators. Defined as individual functions to simplify
    calling and reduce code length.

    Sub: For sub-critical messages, describing things like notes and warnings

    :type val: str
    :param val: formatted message to return
    :rtype: str
    :return: formatted string message to be printed to std out
    """
    sub_ = """{}
--------------------------------------------------------------------------------
"""
    return sub_.format(val)


def cli(text="", items=None, wraplen=80, header=None, border=None, hchar="/"):
    """
    Provide a standardized look to the SeisFlows command line interface messages
    The look we are after is something like:


    $ seisflows cmd

        =======================
                HEADER
                //////
        text

        item1
        item2
        ...
        itemN
        =======================

    $ ls -l

    :type text: str
    :param text: text to format into the cli look
    :type items: list
    :param items: optional list of items that will be displayed on new lines
        after the text. Useful for listing parameters or paths. The items here
        are NOT wrapped.
    :type wraplen: int
    :param wraplen: desired line length to wrap messages.
    :type header: str
    :param header: optional header line that will be centered (wraplen/2) and
        capitalized. Useful for things like 'WARNING' and 'ERROR'
    :type border: str
    :param border: a character to use to block off
    :type hchar: str
    :param hchar: character to underline the header with
    :rtype output_str: str
    :return output_str: formatted string to print out
    """
    # Start with a newline to space from command line arg
    output_str = "\n"
    # Add top border
    if border is not None:
        output_str += f"{border * wraplen}\n"
    # Add header below top border and a line below that
    if header is not None:
        output_str += f"{header.upper():^{wraplen}}\n"
        output_str += f"{hchar * len(header):^{wraplen}}\n"
    # Format the actual input string with a text wrap
    output_str += "\n".join(wrap(text, width=wraplen, break_long_words=False))
    # Add list items in order of list
    if items:
        output_str += "\n\n"
        output_str += "\n".join(items)
    # Add bottom border
    if border is not None:
        output_str += f"\n{border * wraplen}"
    # Final newline to space from next cli
    output_str += "\n"
    return output_str



WarningOverwrite = """

WARNING: Data from previous workflow found in working directory.

To delete data and start a new workflow type:
  seisflows restart

To resume existing workflow type:
  seisflows resume

"""

SystemWarning = """

Please double check SYSTEM parameter

    Expected hostname: {}
    Actual hostname: {}

"""

ParameterWarning_SPECFEM = """

PARAMETER WARNING

    There is a conflict between parameters.

    SPECFEM Parameter:  "{}"
    Old Value:  {}
    Overwriting with:  {}

"""

DataFormatWarning = """

DATA FORMAT WARNING

    reader format: {}
    writer format: {}

    Incompatible file formats may result in job failure or other problems.

"""

TaskIDWarning = """

    WARNING: system.taskid() OS environment variable 'SEISFLOWS_TASKID' not 
    found, SeisFlows3 is assuming debug mode and returning taskid=0. 
    If you are not running in debug mode, please check your SYSTEM.run() or
    SYSTEM.run_single() commands, which are responsible for setting 
    the 'SEISFLOWS_TASKID'

"""

FileError = """

FILE NOT FOUND

    {file}

"""

SolverError = """

SOLVER FAILED

    Nonzero exit status returned by the following command:  
    
    {exc}

    Subsequent tasks may fail because expected solver output is not in place.
    Users running on clusters without fault tolerance should consider stopping 
    any remaining workflow tasks to avoid further loss of resources. 

    To troubleshoot solver errors, navigate to ./scratch/solver to browse solver
    output or try running solver manually in the directories set up in
    ./scratch/solver. 

"""


ReceiverError_SPECFEM = """

ERROR READING RECEIVERS

    Error reading receivers.

"""

SourceError_SPECFEM = """

ERROR READING SOURCES

    In DIRECTORY, there must be one or more files matching WILDCARD.

    DIRECTORY:  "{}"
    WILDCARD:  "{}"

"""


ReaderError = """

READER ERROR

   Seismic data reader not found.

   PAR.READER must correspond to an entry in seisflows.plugins.readers

"""

WriterError = """

WRITER ERROR

   Seismic data writer not found.

   PAR.WRITER must correspond to an entry in seisflows.plugins.writers

"""

TaskTimeout = """

TASK TIMED OUT

    Stopping workflow because task time limit exceeded. (To adjust limit,
    add or modify TASKTIME in parameter file.)

        Task name:  {classname}.{method}
        Task id:    {job_id}
        Time limit (minutes): {tasktime}

"""

TaskError_LSF = """

TASK ERROR

    Task failed:  {}.{}

    For more information, see output.lsf/{}

    Stopping workflow...

"""


TaskError_PBS = """

TASK ERROR

    Task failed:  {}.{}

    For more information, see output.pbs/{}

    Stopping workflow...

"""

TaskError_SLURM = """

TASK ERROR

    Task failed:  {classname}.{method}

    For more information, see output.logs/{job_id}

    Stopping workflow...

"""

obspyImportError = """

DEPENDENCY ERROR

    The current data processing workflow requires OBSPY.  Please install it and
    try again.

"""

mpiError1 = """

SYSTEM CONFIGURATION ERROR

    The following system configuration can be used only with single-core
    solvers:

        system.{}

    If your solver requires only a single core, then set NPROC equal to 1.

    If your solver requires multiple cores, then consider using lsf_lg, pbs_lg,
    or slurm_lg system configurations instead.

"""

mpiError2 = """

DEPENDENCY ERROR

    The following system configuration requires MPI4PY:

        system.{}

    Please install MPI4PY and try again, or consider choosing a different system
    configuration.

"""

mpiError3 = """

SYSTEM CONFIGURATION WARNING

    The following system configuration requires 'mpiexec':

        system.{}

    Please make sure than 'mpiexec' is accessible through your shell's PATH
    environment variable. If your executable goes by a different name such as
    'mpirun', consider creating an alias in your shell's configuration file, and
    remember to source the modified configuration file. If MPI is not available
    on your system, consider using the 'multithreaded' system interface instead.

"""

MissingParameter_Workflow = """

Please specify a workflow by adding a line to the parameter file, e.g.

    WORKFLOW='inversion';

for a list of available workflows, see seisflows/workflow in the source code

"""

MissingParameter_System = """

Please specify a system interface by adding a line to the parameter file, e.g.

    SYSTEM='serial';

for a list of available interfaces, see seisflows/system in the source code

"""

ImportError1 = """

SEISFLOWS IMPORT ERROR

    Please check that "custom_import" utility is being used as follows:

        custom_import(name1, name2)

    The resulting full dotted name "seisflows.name1.name2" must correspond to a
    module in the SeisFlows package.

"""

ImportError2 = """

SEISFLOWS IMPORT ERROR

    custom_import(system, classname, method)

    Please check that "name1" is one of the following

        workflow
        solver
        optimize
        preprocess
        postprocess
        system

"""

ImportError3 = """

SEISFLOWS IMPORT ERROR

    The following module was not found in the SeisFlows package:

        seisflows.{name}.{module}

    Please check user-supplied {module_upper} parameter.

"""

ImportError4 = """

SEISFLOWS IMPORT ERROR

    By convention, SeisFlows module 

        seisflows.{name}.{module}

    must contain a class named

        {classname}

"""

CompatibilityError1 = """

Parameter settings have changed.

In your parameter file, please remove
    OPTIMIZE='base'

and add one of the following instead
    OPTIMIZE='LBFGS'
    OPTIMIZE'=NLCG'
    OPTIMIZE='SteepestDescent'

"""

Warning_pbs_sm = """

WARNING:  PBS_SM hasn't been tested for a long while because we don't own a PBS
cluster.  If you have access to one cluster and are willing to help debug, 
please let us know.

"""

Warning_pbs_lg = """

WARNING:  PBS_LG hasn't been tested for a long while because we don't own a PBS
cluster.  If you have access to one cluster and are willing to help debug, 
please let us know.

"""

PoissonsRatioError = """
                
ERROR CHECKING POISSON'S RATIO

    The Poisson's ratio of the given model is out of bounds with respect 
    to the defined range ({min_val}, {max_val}). The model bounds were found 
    to be:

    {pmin:.2f} < PR < {pmax:.2f}

"""

ExportResidualsError = """

PREPROCESSING ERROR

    The Solver function 'export_residuals' expected 'residuals' directories to 
    be created but could not find them and cannot continue the workflow. 
    
    Please check the preprocess.prepare_eval_grad() function which is
    responsible for exporting the 'residuals' directory. Or use 
    'seisflows debug' to investigate the error more closely.


"""


DataFilenamesError = """

    ERROR: The property solver.data_filenames, which is used to search for 
    trace data in ./scratch/solver/*/traces is empty and should not be. 
    Please check solver.data_filenames and solver.data_wildcard against filenames
    in the traces/ directory.
    

"""


def check(cls):
    """
    Standardized log message sent from the check() function that is required
    within each module and submodule. Simply notifies the user that checks
    are being performed within the given module

    :type cls: 'type'
    :param cls: self.__class__ or type(self) which should be passed in from
        INSIDE a function defined INSIDE a class.
        e.g., <class 'seisflows3.preprocess.default.Default'>
    :rtype: str
    :return: formatted check string describing the module and classname
        e.g., preprocess.default
    """
    module, clsname = split_cls(cls)
    return f"check paths/pars module: {module}.{clsname}"


def setup(cls):
    """
    Standardized log message sent from the setup() function that is required
    within each module and submodule. Simply notifies the user that checks
    are being performed within the given module

    :type cls: 'type'
    :param cls: self.__class__ which should be passed in from INSIDE a function
        defined INSIDE a class.
        e.g., <class 'seisflows3.preprocess.default.Default'>
    :rtype: str
    :return: formatted string describing the module and classname
        e.g., preprocess.default

    """
    module, clsname = split_cls(cls)
    return f"setting up module: {module}.{clsname}"


def whoami(cls, append="", prepend=""):
    """
    Standardized log message sent from any function inside a class. Used in logs
    for subclasses to declare who they are before running functions, makes it
    easier to track down what's happening where

    :type cls: 'type'
    :param cls: self.__class__ which should be passed in from INSIDE a function
        defined INSIDE a class.
        e.g., <class 'seisflows3.preprocess.default.Default'>
    :type append: str
    :param append: add any string after the whoami statement
    :type prepend: str
    :param prepend: add any string in front of the whoami statment
    :rtype: str
    :return: formatted string describing the module and classname
        e.g., preprocess.default
    """
    module, clsname = split_cls(cls)
    return f"{prepend}{module}.{clsname}{append}"


def split_cls(cls):
    """
    Repeatedly used function to split the output of type(self) or self.__class__
    into separate strings


    :type cls: 'type'
    :param cls: self.__class__ which should be passed in from INSIDE a function
        defined INSIDE a class.
        e.g., <class 'seisflows3.preprocess.default.Default'>
    :rtype: tuple of strings
    :return: module, classname
    """
    type_, str_, brkt = str(cls).split("'")
    sf3, module, fid, clsname = str_.split(".")
    return module, clsname