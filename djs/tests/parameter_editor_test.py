#! /usr/bin/env python3

import unittest


class TestParameterMethods(unittest.TestCase):
    def test_perturb_parameters(self):

        from os.path import abspath, dirname, join
        import xarray as xr

        # Local imports
        from djs.perturbation_engine.parameter_editor import (
            perturb_parameters,
            _map_to_operator,
        )

        current_dir = abspath(dirname(__file__))

        # Path to pocono test case from relative location
        test_case_dir = abspath(join(current_dir, "..", "..", "pocono_test_case"))

        route_link_fn = join(test_case_dir, "Route_Link.nc")
        parameter_op_dict = {"n": [("^", 1.0), ("+", 2.0)]}

        operators = ["^", "+"]
        values = [1, 2]

        # Get first index for the mannings n parameter
        df_0 = xr.open_dataset(route_link_fn).n.values[0]

        # Apply the functions defined above in operators and values to df_0
        for i, op in enumerate(operators):
            func = _map_to_operator(op)
            df_0 = func(df_0, values[i])

        df = perturb_parameters(route_link_fn, parameter_op_dict).n.values[0]

        self.assertAlmostEqual(df, df_0, places=5)

    def test__apply_functions(self):

        import xarray as xr

        # import numpy as np
        from os.path import abspath, dirname, join

        # from scipy.stats import norm

        # Local imports
        from djs.perturbation_engine.parameter_editor import (
            # _map_to_operator,
            _apply_functions,
        )

        current_dir = abspath(dirname(__file__))

        # Path to pocono test case from relative location
        test_case_dir = abspath(join(current_dir, "..", "..", "pocono_test_case"))
        route_link_fn = join(test_case_dir, "Route_Link.nc")

        df = xr.open_dataset(route_link_fn)

        apply_dict = {"n": [("norm", False), ("+", 17)], "nCC": [("-", 9)]}

        df_0 = _apply_functions(df, apply_dict)

        print(df_0)

        # self.assertAlmostEqual(df, rvs)

    def test__apply_dists(self):

        import xarray as xr

        # import numpy as np
        from os.path import abspath, dirname, join

        # Local imports
        from djs.perturbation_engine.parameter_editor import (
            # _map_to_operator,
            _apply_dists,
        )

        current_dir = abspath(dirname(__file__))

        # Path to pocono test case from relative location
        test_case_dir = abspath(join(current_dir, "..", "..", "pocono_test_case"))
        route_link_fn = join(test_case_dir, "Route_Link.nc")
        fulldom_hires_fn = join(test_case_dir, "primary", "DOMAIN", "Fulldom_hires.nc")

        df = xr.open_dataset(route_link_fn)
        df_fulldom = xr.open_dataset(fulldom_hires_fn)

        dist_dict_0 = {"n": ["norm", True]}
        dist_dict_1 = {"n": ["norm", False]}
        dist_dict_2 = {"LKSATFAC": ["uniform", True]}
        dist_dict_3 = {"LKSATFAC": ["uniform", False]}

        df_0 = _apply_dists(df, dist_dict_0)
        df_1 = _apply_dists(df, dist_dict_1)
        df_2 = _apply_dists(df_fulldom, dist_dict_2)
        df_3 = _apply_dists(df_fulldom, dist_dict_3)


if __name__ == "__main__":
    unittest.main()
