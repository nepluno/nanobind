import test_stl_ext as t
import pytest
import gc

@pytest.fixture
def clean():
    gc.collect()
    t.reset()

def assert_stats(**kwargs):
    gc.collect()
    for k, v in t.stats().items():
        fail = False
        if k in kwargs:
            if v != kwargs[k]:
                fail = True
        elif v != 0:
            fail = True
        if fail:
            raise Exception(f'Mismatch for key {k}: {t.stats()}')


# ------------------------------------------------------------------
# The following aren't strictly STL tests, but they are helpful in
# ensuring that move constructors/copy constructors of bound C++ types
# are properly triggered, which the STL type casters depend on.
# ------------------------------------------------------------------

def test01_movable_return(clean):
    assert t.return_movable().value == 5
    assert_stats(
        default_constructed=1,
        move_constructed=1,
        destructed=2)


def test02_movable_return_ptr(clean):
    assert t.return_movable_ptr().value == 5
    assert_stats(
        default_constructed=1,
        destructed=1)


def test03_movable_in_value(clean):
    s = t.Movable()
    t.movable_in_value(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2)


def test04_movable_in_lvalue_ref(clean):
    s = t.Movable()
    t.movable_in_lvalue_ref(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        destructed=1)


def test05_movable_in_ptr(clean):
    s = t.Movable()
    t.movable_in_ptr(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        destructed=1)


def test06_movable_in_rvalue_ref(clean):
    s = t.Movable()
    t.movable_in_rvalue_ref(s)
    assert s.value == 0
    del s
    assert_stats(
        default_constructed=1,
        move_constructed=1,
        destructed=2)


def test07_copyable_return(clean):
    assert t.return_copyable().value == 5
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2)


def test08_copyable_return_ptr(clean):
    assert t.return_copyable_ptr().value == 5
    assert_stats(
        default_constructed=1,
        destructed=1)


def test09_copyable_in_value(clean):
    s = t.Copyable()
    t.copyable_in_value(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2)


def test10_copyable_in_lvalue_ref(clean):
    s = t.Copyable()
    t.copyable_in_lvalue_ref(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        destructed=1)


def test11_copyable_in_ptr(clean):
    s = t.Copyable()
    t.copyable_in_ptr(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        destructed=1)


def test12_copyable_in_rvalue_ref(clean):
    s = t.Copyable()
    t.copyable_in_rvalue_ref(s)
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2)

# ------------------------------------------------------------------

def test13_tuple_movable_return(clean):
    assert t.tuple_return_movable()[0].value == 5
    assert_stats(
        default_constructed=1,
        move_constructed=2,
        destructed=3)


def test14_tuple_movable_return_ptr(clean):
    assert t.return_movable_ptr().value == 5
    assert_stats(
        default_constructed=1,
        destructed=1)


def test15_tuple_movable_in_value(clean):
    s = t.Movable()
    t.tuple_movable_in_value((s,))
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2)


def test16_tuple_movable_in_lvalue_ref(clean):
    s = t.Movable()
    t.tuple_movable_in_lvalue_ref((s,))
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        destructed=1)


def test17_tuple_movable_in_lvalue_ref_2(clean):
    s = t.Movable()
    t.tuple_movable_in_lvalue_ref_2((s,))
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2)


def test18_tuple_movable_in_ptr(clean):
    s = t.Movable()
    t.tuple_movable_in_ptr((s,))
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        destructed=1)


def test19_tuple_movable_in_rvalue_ref(clean):
    s = t.Movable()
    t.tuple_movable_in_rvalue_ref((s,))
    assert s.value == 0
    del s
    assert_stats(
        default_constructed=1,
        move_constructed=1,
        destructed=2)


def test20_tuple_movable_in_rvalue_ref_2(clean):
    s = t.Movable()
    t.tuple_movable_in_rvalue_ref_2((s,))
    assert s.value == 5
    del s
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        move_constructed=1,
        destructed=3)

# ------------------------------------------------------------------

def test21_tuple_pair_basic():
    assert t.empty_tuple(()) == ()
    assert t.swap_tuple((1, 2.5)) == (2.5, 1)
    assert t.swap_pair((1, 2.5)) == (2.5, 1)

# ------------------------------------------------------------------

def test22_vec_return_movable(clean):
    for i, x in enumerate(t.vec_return_movable()):
        assert x.value == i
    del x
    assert_stats(
        value_constructed=10,
        move_constructed=10,
        destructed=20
    )


def test23_vec_return_copyable(clean):
    for i, x in enumerate(t.vec_return_copyable()):
        assert x.value == i
    del x
    assert_stats(
        value_constructed=10,
        copy_constructed=20,
        destructed=30
    )


def test24_vec_movable_in_value(clean):
    t.vec_moveable_in_value([t.Movable(i) for i in range(10)])
    assert_stats(
        value_constructed=10,
        copy_constructed=10,
        move_constructed=10,
        destructed=30
    )


def test25_vec_movable_in_value(clean):
    t.vec_copyable_in_value([t.Copyable(i) for i in range(10)])
    assert_stats(
        value_constructed=10,
        copy_constructed=20,
        destructed=30
    )


def test26_vec_movable_in_lvalue_ref(clean):
    t.vec_moveable_in_lvalue_ref([t.Movable(i) for i in range(10)])
    assert_stats(
        value_constructed=10,
        move_constructed=10,
        destructed=20
    )


def test27_vec_movable_in_ptr_2(clean):
    t.vec_moveable_in_ptr_2([t.Movable(i) for i in range(10)])
    assert_stats(
        value_constructed=10,
        destructed=10
    )


def test28_vec_movable_in_rvalue_ref(clean):
    t.vec_moveable_in_rvalue_ref([t.Movable(i) for i in range(10)])
    assert_stats(
        value_constructed=10,
        move_constructed=10,
        destructed=20
    )

def test29_opaque_vector():
    f = t.float_vec()
    assert f.size() == 0
    assert isinstance(f, t.float_vec)
    f.push_back(1)
    assert f.size() == 1


def test30_std_function():
    assert t.return_empty_function() is None
    assert t.return_function()(3) == 8
    assert t.call_function(lambda x: 5 + x, 3) == 8

    with pytest.raises(TypeError) as excinfo:
        assert t.call_function(5, 3) == 8
    assert 'incompatible function arguments' in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        assert t.call_function(lambda x, y: x+y, 3) == 8
    assert 'missing 1 required positional argument' in str(excinfo.value)


def test31_vec_type_check():
    with pytest.raises(TypeError) as excinfo:
        t.vec_moveable_in_value(0)

def test32_list():
    assert t.identity_list([]) == []
    assert t.identity_list([1, 2, 3]) == [1, 2, 3]
    assert t.identity_list(()) == []
    assert t.identity_list((1, 2, 3)) == [1, 2, 3]

def test33_string_and_string_view():
    assert t.identity_string("") == ""
    assert t.identity_string("orange") == "orange"
    assert t.identity_string("橘子") == "橘子"
    assert t.identity_string("ส้ม") == "ส้ม"
    assert t.identity_string("البرتقالي") == "البرتقالي"
    assert t.identity_string("🍊") == "🍊"

    assert t.identity_string_view("") == ""
    assert t.identity_string_view("orange") == "orange"
    assert t.identity_string_view("橘子") == "橘子"
    assert t.identity_string_view("ส้ม") == "ส้ม"
    assert t.identity_string_view("البرتقالي") == "البرتقالي"
    assert t.identity_string_view("🍊") == "🍊"

def test34_std_optional_copyable(clean):
    t.optional_copyable(t.Copyable())
    assert t.optional_copyable.__doc__ == (
        "optional_copyable(x: Optional[test_stl_ext.Copyable]) -> None"
    )
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2
    )

def test35_std_optional_copyable_ptr(clean):
    t.optional_copyable_ptr(t.Copyable())
    assert t.optional_copyable_ptr.__doc__ == (
        "optional_copyable_ptr(x: Optional[test_stl_ext.Copyable]) -> None"
    )
    assert_stats(
        default_constructed=1,
        destructed=1
    )

def test36_std_optional_none():
    t.optional_none(None)

def test37_std_optional_ret_opt_movable(clean):
    assert t.optional_ret_opt_movable().value == 5
    assert t.optional_ret_opt_movable.__doc__ == (
        "optional_ret_opt_movable() -> Optional[test_stl_ext.Movable]"
    )
    assert_stats(
        default_constructed=1,
        move_constructed=2,
        destructed=3
    )

def test38_std_optional_ret_opt_movable_ptr(clean):
    assert t.optional_ret_opt_movable_ptr().value == 5
    assert_stats(
        default_constructed=1,
        destructed=1
    )

def test39_std_optional_ret_opt_none():
    assert t.optional_ret_opt_none() is None

def test40_std_optional_unbound_type():
    assert t.optional_unbound_type(3) == 3
    assert t.optional_unbound_type(None) is None
    assert t.optional_unbound_type() is None
    assert t.optional_unbound_type.__doc__ == (
        "optional_unbound_type(x: Optional[int] = None) -> Optional[int]"
    )

def test41_std_variant_copyable(clean):
    t.variant_copyable(t.Copyable())
    t.variant_copyable(5)
    assert t.variant_copyable.__doc__ == (
        "variant_copyable(arg: Union[test_stl_ext.Copyable, int], /) -> None"
    )
    assert_stats(
        default_constructed=3,
        copy_assigned=1,
        destructed=3
    )

def test42_std_variant_copyable_none(clean):
    t.variant_copyable_none(t.Copyable())
    t.variant_copyable_none(5)
    t.variant_copyable_none(None)
    assert t.variant_copyable_none.__doc__ == (
        "variant_copyable_none(x: Optional[Union[test_stl_ext.Copyable, int]]) -> None"
    )
    assert_stats(
        default_constructed=1,
        copy_constructed=1,
        destructed=2
    )

def test43_std_variant_copyable_ptr(clean):
    t.variant_copyable_ptr(t.Copyable())
    t.variant_copyable_ptr(5)
    assert t.variant_copyable_ptr.__doc__ == (
        "variant_copyable_ptr(arg: Union[test_stl_ext.Copyable, int], /) -> None"
    )
    assert_stats(
        default_constructed=1,
        destructed=1
    )

def test44_std_variant_copyable_ptr_none(clean):
    t.variant_copyable_ptr_none(t.Copyable())
    t.variant_copyable_ptr_none(5)
    t.variant_copyable_ptr_none(None)
    assert t.variant_copyable_ptr_none.__doc__ == (
        "variant_copyable_ptr_none(x: Optional[Union[test_stl_ext.Copyable, int]]) -> None"
    )
    assert_stats(
        default_constructed=1,
        destructed=1
    )

def test45_std_variant_ret_var_copyable(clean):
    assert t.variant_ret_var_copyable().value == 5
    assert t.variant_ret_var_copyable.__doc__ == (
        "variant_ret_var_copyable() -> Union[test_stl_ext.Copyable, int]"
    )

def test46_std_variant_ret_var_none(clean):
    assert t.variant_ret_var_none() is None
    assert t.variant_ret_var_none.__doc__ == (
        "variant_ret_var_none() -> Union[None, test_stl_ext.Copyable, int]"
    )

def test47_std_variant_unbound_type(clean):
    assert t.variant_unbound_type() is None
    assert t.variant_unbound_type(None) is None
    assert t.variant_unbound_type([5]) == [5]
    assert t.variant_unbound_type((1,2,3)) == (1,2,3)
    assert t.variant_unbound_type(5) == 5
    assert t.variant_unbound_type.__doc__ == (
        "variant_unbound_type(x: Optional[Union[list, tuple, int]] = None)"
        " -> Union[None, list, tuple, int]"
    )

def test48_map_return_movable_value(clean):
    for i, (k, v) in enumerate(sorted(t.map_return_movable_value().items())):
        assert k == chr(ord("a") + i)
        assert v.value == i
    assert t.map_return_movable_value.__doc__ == (
        "map_return_movable_value() -> dict[str, test_stl_ext.Movable]"
    )

def test49_map_return_copyable_value(clean):
    for i, (k, v) in enumerate(sorted(t.map_return_copyable_value().items())):
        assert k == chr(ord("a") + i)
        assert v.value == i
    assert t.map_return_copyable_value.__doc__ == (
        "map_return_copyable_value() -> dict[str, test_stl_ext.Copyable]"
    )

def test50_map_movable_in_value(clean):
    t.map_movable_in_value(dict([(chr(ord("a") + i), t.Movable(i)) for i in range(10)]))
    assert t.map_movable_in_value.__doc__ == (
        "map_movable_in_value(x: dict[str, test_stl_ext.Movable]) -> None"
    )

def test51_map_movable_in_value(clean):
    t.map_copyable_in_value(dict([(chr(ord("a") + i), t.Copyable(i)) for i in range(10)]))
    assert t.map_copyable_in_value.__doc__ == (
        "map_copyable_in_value(x: dict[str, test_stl_ext.Copyable]) -> None"
    )

def test52_map_movable_in_lvalue_ref(clean):
    t.map_movable_in_lvalue_ref(dict([(chr(ord("a") + i), t.Movable(i)) for i in range(10)]))
    assert t.map_movable_in_lvalue_ref.__doc__ == (
        "map_movable_in_lvalue_ref(x: dict[str, test_stl_ext.Movable]) -> None"
    )

def test53_map_movable_in_rvalue_ref(clean):
    t.map_movable_in_rvalue_ref(dict([(chr(ord("a") + i), t.Movable(i)) for i in range(10)]))
    assert t.map_movable_in_rvalue_ref.__doc__ == (
        "map_movable_in_rvalue_ref(x: dict[str, test_stl_ext.Movable]) -> None"
    )

def test54_map_movable_in_ptr(clean):
    t.map_movable_in_ptr(dict([(chr(ord("a") + i), t.Movable(i)) for i in range(10)]))
    assert t.map_movable_in_ptr.__doc__ == (
        "map_movable_in_ptr(x: dict[str, test_stl_ext.Movable]) -> None"
    )
