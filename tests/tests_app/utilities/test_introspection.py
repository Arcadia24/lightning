import os
from numbers import Rational

from lightning_app import LightningApp, LightningFlow
from lightning_app.testing.helpers import _RunIf
from lightning_app.utilities.imports import _is_pytorch_lightning_available
from lightning_app.utilities.introspection import Scanner

if _is_pytorch_lightning_available():
    from pytorch_lightning import Trainer
    from pytorch_lightning.cli import LightningCLI

from tests_app import _PROJECT_ROOT


def test_introspection():
    """This test validates the scanner can find some class within the provided files."""

    scanner = Scanner(str(os.path.join(_PROJECT_ROOT, "tests/tests_app/core/scripts/example_1.py")))
    assert scanner.has_class(Rational)
    assert not scanner.has_class(LightningApp)

    scanner = Scanner(str(os.path.join(_PROJECT_ROOT, "tests/tests_app/core/scripts/example_2.py")))
    assert scanner.has_class(LightningApp)
    assert not scanner.has_class(LightningFlow)


@_RunIf(pl=True)
def test_introspection_lightning():
    """This test validates the scanner can find some PyTorch Lightning class within the provided files."""
    scanner = Scanner(str(os.path.join(_PROJECT_ROOT, "tests/tests_app/core/scripts/lightning_cli.py")))
    assert not scanner.has_class(Trainer)
    assert scanner.has_class(LightningCLI)

    scanner = Scanner(str(os.path.join(_PROJECT_ROOT, "tests/tests_app/core/scripts/lightning_trainer.py")))
    assert scanner.has_class(Trainer)
    assert not scanner.has_class(LightningCLI)


@_RunIf(pl=True)
def test_introspection_lightning_overrides():
    """This test validates the scanner can find all the subclasses from primitives classes from PyTorch Lightning
    in the provided files."""
    scanner = Scanner(str(os.path.join(_PROJECT_ROOT, "tests/tests_app/core/scripts/lightning_cli.py")))
    scan = scanner.scan()
    assert set(scan) == {"LightningDataModule", "LightningModule"}

    scanner = Scanner(str(os.path.join(_PROJECT_ROOT, "tests/tests_app/core/scripts/lightning_overrides.py")))
    scan = scanner.scan()
    assert set(scan) == {
        "Accelerator",
        "Profiler",
        "Callback",
        "LightningDataModule",
        "LightningLite",  # deprecated
        "Fabric",
        "Logger",
        "LightningModule",
        "Loop",
        "Metric",
        "PrecisionPlugin",
        "Trainer",
    }
