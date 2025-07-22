import pytest
import os
import datetime

@pytest.hookimpl(tryfirst=True)
def _pytest_configure(config):
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = os.path.join(report_dir, f"report_{now}.html")

    config.option.htmlpath = report_file
    config.option.self_contained_html = True

def pytest_metadata(metadata):
    metadata['Project'] = 'API Automation with Pytest'
    metadata['Author'] = 'Tisna Hidayat'
    metadata['Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata['Environment'] = 'Development'
    metadata['Version'] = '1.0.0'

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    print("Setup module")
    yield
    print("Teardown module")

