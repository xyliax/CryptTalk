use pyo3::prelude::*;
pub fn from_python() -> String {
    let py_rsa = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/security/rsa.py"));
    let from_python = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
        let app: Py<PyAny> = PyModule::from_code(py, py_rsa, "", "")?
            .getattr("run")?
            .into();
        app.call0(py)
    })
    .unwrap();

    format!("py: {}", from_python)
}
