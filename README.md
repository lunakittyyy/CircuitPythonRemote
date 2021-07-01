# CircuitPythonRemote
Basic remote using CircuitPython, made with the CPX in mind but it should work on other CircuitPython compatible boards

Lines 12 through 23 are all the arrays for IR listening. If the recieved array is within a fuzziness threshold of 0.2, it will pass it on to the rest of the code and trigger the corrosponding media key.
