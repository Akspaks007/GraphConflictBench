from pathlib import Path

import pytest

from graphconflictbench.reasoner import Ontology

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def ontology():
    return Ontology.load(ROOT / "configs/ontology.yaml")
