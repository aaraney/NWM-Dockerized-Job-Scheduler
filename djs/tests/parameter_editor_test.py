#! /usr/bin/env python3

import unittest

class TestParameterMethods(unittest.TestCase):

    def test_edit_parameters(self):

        from os.path import abspath, dirname, join
        import xarray as xr

        # Local imports
        from djs.perturbation_engine.parameter_editor import edit_parameters, _map_to_operator

        current_dir = abspath(dirname(__file__))

        # Path to pocono test case from relative location
        test_case_dir = abspath(join(current_dir, '..', '..', 'pocono_test_case'))

        route_link_fn = join(test_case_dir, 'Route_Link.nc')
        parameters = ['n', 'n']
        operators = ['^', '+']
        values = [1, 2]


        # Get first index for the mannings n parameter
        df_0 = xr.open_dataset(route_link_fn).n.values[0]

        # Apply the functions defined above in operators and values to df_0
        for i, op in enumerate(operators):
            func = _map_to_operator(op)
            df_0 = func(df_0, values[i])

        df = edit_parameters(route_link_fn, parameters, operators, values).n.values[0]

        self.assertAlmostEqual(df, df_0, places=5)


if __name__ == "__main__":
    unittest.main()