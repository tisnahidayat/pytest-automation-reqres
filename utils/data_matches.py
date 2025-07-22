
def assert_user_data_matches(actual_data, expected_data):
    for key in expected_data:
        assert key in actual_data, f"Missing field: {key}"
        assert isinstance(actual_data[key], (str, int)), f"{key} has invalid type"
        assert actual_data[key] is not None, f"{key} should not be None"
        assert actual_data[key] == expected_data[key], f"{key} mismatch: expected {expected_data[key]}, got {actual_data[key]}"
    