#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *cvarint_encode(PyObject *self, PyObject *args) {
    // int ok;
    unsigned long long int n;
    PyArg_ParseTuple(args, "K", &n);
    
    char buffer[10];
    int index = 0;

    while (n > 0x7f) {
        buffer[index++] = (n & 0x7f) | 0x80;
        n >>= 7;
    }

    buffer[index++] = n & 0x7f;

    return PyBytes_FromStringAndSize(buffer, index);
}

static PyObject *cvarint_decode(PyObject *self, PyObject *args) {
    char *buffer;
    Py_ssize_t length;
    PyArg_ParseTuple(args, "s#", &buffer, &length);

    unsigned long long int n = 0;

    while (length > 0) {
        // buff = buffer[length-1];
        n <<= 7;
        n |= buffer[length-1] & 0x7f;
        length--;
    }

    return PyLong_FromUnsignedLongLong(n);
}

static PyMethodDef CVarintMethods[] = {
    {"encode", cvarint_encode, METH_VARARGS, "Encode an integer as varint."},
    {"decode", cvarint_decode, METH_VARARGS,
     "Decode varint bytes to an integer."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cvarintmodule = {
    PyModuleDef_HEAD_INIT, "cvarint",
    "A C implementation of protobuf varint encoding", -1, CVarintMethods};

PyMODINIT_FUNC PyInit_cvarint(void) { return PyModule_Create(&cvarintmodule); }
