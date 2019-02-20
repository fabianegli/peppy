""" Regression tests related to subproject activation behavior """

import mock
import os
import random
import string
import pytest
import yaml
from peppy import Project
from peppy import SAMPLE_ANNOTATIONS_KEY
from peppy.const import METADATA_KEY


__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


_PARENT_ANNS = "sample_annotation.csv"
_CHILD_ANNS = "sample_annotation_sp1.csv"
_SP_NAME = "dog"


def touch(folder, name):
    fp = os.path.join(folder, name)
    with open(fp, 'w'):
        return fp


@pytest.fixture(scope="function")
def conf_data(tmpdir):
    d = tmpdir.strpath
    parent_sheet_file = touch(d, _PARENT_ANNS)
    child_sheet_file = touch(d, _CHILD_ANNS)
    return {
        METADATA_KEY: {
            SAMPLE_ANNOTATIONS_KEY: parent_sheet_file,
            "output_dir": tmpdir.strpath,
            "pipeline_interfaces": tmpdir.strpath
        },
        "subprojects": {
            _SP_NAME: {METADATA_KEY: {SAMPLE_ANNOTATIONS_KEY: child_sheet_file}}
        }
    }


@pytest.fixture(scope="function")
def conf_file(tmpdir, conf_data):
    conf = tmpdir.join("".join(
        [random.choice(string.ascii_letters) for _ in range(20)])).strpath
    with open(conf, 'w') as f:
        yaml.dump(conf_data, f)
    return conf


class SubprojectSampleAnnotationTests:
    """ Tests concerning sample annotations path when a subproject is used. """

    @staticmethod
    def test_annotations_path_is_from_subproject(conf_file):
        """ Direct Project construction with subproject points to anns file. """
        p = Project(conf_file, subproject=_SP_NAME)
        _, anns_file = os.path.split(p.metadata.sample_annotation)
        assert _CHILD_ANNS == anns_file

    @staticmethod
    def test_subproject_activation_updates_sample_annotations_path(conf_file):
        """ Subproject's sample annotation file pointer replaces original. """
        p = Project(conf_file)
        p.activate_subproject(_SP_NAME)
        _, anns_file = os.path.split(p.metadata.sample_annotation)
        assert _CHILD_ANNS == anns_file
