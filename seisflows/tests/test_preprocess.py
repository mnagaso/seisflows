"""
Test the ability of the Solver module to interact with various versions of
SPECFEM
"""
import os
import pytest
from glob import glob
from seisflows import ROOT_DIR
from seisflows.preprocess.default import Default


TEST_DATA = os.path.join(ROOT_DIR, "tests", "test_data", "test_preprocess")


def test_read():
    """
    Test that we can read SPECFEM generated synthetics with the preprocess mod.
    """
    # If new data formats are added to preprocess, they need to be tested
    tested_data_formats = ["ASCII", "SU"]
    preprocess = Default()
    assert(set(tested_data_formats) == set(preprocess._acceptable_data_formats))

    preprocess = Default(data_format="ascii")
    st1 = preprocess.read(os.path.join(TEST_DATA, "AA.S0001.BXY.semd"))

    preprocess = Default(data_format="su")
    st2 = preprocess.read(os.path.join(TEST_DATA, "Uy_file_single_d.su"))

    assert(st1[0].stats.npts == st2[0].stats.npts)


def test_write(tmpdir):
    """
    Make sure we can write both data formats
    """
    # If new data formats are added to preprocess, they need to be tested
    tested_data_formats = ["ASCII", "SU"]
    preprocess = Default()
    assert(set(tested_data_formats) == set(preprocess._acceptable_data_formats))

    preprocess = Default(data_format="ascii")
    st1 = preprocess.read(os.path.join(TEST_DATA, "AA.S0001.BXY.semd"))
    preprocess.write(st1, fid=os.path.join(tmpdir, "test_stream_ascii"))

    preprocess.data_format = "SU"
    preprocess.write(st1, fid=os.path.join(tmpdir, "test_stream_su"))


def test_initialize_adjoint_traces(tmpdir):
    """
    Make sure we can write empty adjoint sources expected by SPECFEM
    """
    preprocess = Default(data_format="ascii")
    data_filenames = glob(os.path.join(TEST_DATA, "*semd"))
    preprocess.initialize_adjoint_traces(data_filenames=data_filenames,
                                         output=tmpdir)

    preprocess.data_format = "SU"
    data_filenames = glob(os.path.join(TEST_DATA, "*su"))
    preprocess.initialize_adjoint_traces(data_filenames=data_filenames,
                                         output=tmpdir)

    assert(len(glob(os.path.join(tmpdir, "*"))) == 2)
    for fid in glob(os.path.join(tmpdir, "*")):
        assert(fid.endswith(".adj"))


def test_quantify_misfit(tmpdir):
    """
    Quantify misfit with some example data
    """
    preprocess = Default(data_format="ascii", misfit="waveform",
                         adjoint="waveform", path_preprocess=tmpdir)
    preprocess.setup()

    data_filenames = glob(os.path.join(TEST_DATA, "*semd"))
    preprocess.quantify_misfit(
        observed=data_filenames, synthetic=data_filenames,
        save_residuals=os.path.join(tmpdir, "residuals_ascii"),
        save_adjsrcs=tmpdir
    )

    preprocess.data_format = "SU"
    data_filenames = glob(os.path.join(TEST_DATA, "*su"))
    preprocess.quantify_misfit(
        observed=data_filenames, synthetic=data_filenames,
        save_residuals=os.path.join(tmpdir, "residuals_su"),
        save_adjsrcs=tmpdir
    )

    assert(len(glob(os.path.join(tmpdir, "*"))) == 4)
    residuals = open(os.path.join(tmpdir, "residuals_ascii")).readlines()
    assert(len(residuals) == 1)
    assert(float(residuals[0]) == 0)
