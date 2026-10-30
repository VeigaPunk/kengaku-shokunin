# C1MutClassifier — survivors (mutants no detector killed)

22 of 42 mutants survive all three detectors. Each entry names the case that should have killed it.

## `M01-join-KN-to-K` — join lattice

- mutation: join() maps {K,N} to N instead of K (one comparison result flipped)
- mutated site executes **0 times** over the three corpora (in 0 cases)
- the case that should have killed it — **CLASS moves**: join(K,N): a ternary whose branches are a constant and a name picked out of a listing

```python
def test_f():
    names = os.listdir(D)
    x = 1 if True else names[0]
    assert x
```

  - pristine: `{'test_f': 'P1'}` reasons [[]]
  - mutant:   `{'test_f': 'P0'}` reasons [['assertion depends on no path state (constant/computed value)@9']]

## `M02-join-KL-to-N` — join lattice

- mutation: join() maps {K,L}/{N,L} to N instead of L
- mutated site executes **0 times** over the three corpora (in 0 cases)
- the case that should have killed it — **CLASS moves**: join(K,L): a ternary whose branches are a constant and a listing, compared to a name

```python
def test_f():
    x = 1 if True else os.listdir(D)
    assert x == 'a'
```

  - pristine: `{'test_f': 'P0'}` reasons [['equality on a listing (exact contents/count/emptiness)@8', 'assertion depends on content/value/unknown@8']]
  - mutant:   `{'test_f': 'P1'}` reasons [[]]

## `M03-join-BQ-to-B` — join lattice

- mutation: join() maps {B,Q} to B instead of Q
- mutated site executes **0 times** over the three corpora (in 0 cases)
- the case that should have killed it — **CLASS moves**: join(B,Q): a ternary whose branches are an existence predicate and a qualified-predicate generator, compared

```python
def test_f():
    x = os.path.exists(OUT) if True else (os.path.exists(p) for p in ['/a'])
    assert x == True
```

  - pristine: `{'test_f': 'P0'}` reasons [['value comparison@8', 'assertion depends on content/value/unknown@8']]
  - mutant:   `{'test_f': 'P1'}` reasons [[]]

## `M04-join_all-empty-to-X` — join lattice

- mutation: join_all() of an empty set is X instead of K (default kind dropped)
- mutated site executes **1548 times** over the three corpora (in 282 cases)
- the case that should have killed it — **REASON only**: fuzzer grid 

```python
def h():
    pass
def test_f():
    assert h() is None
```

  - pristine: `{'test_f': 'P0'}` reasons [['value comparison of computed values@9', 'assertion depends on content/value/unknown@9']]
  - mutant:   `{'test_f': 'P0'}` reasons [['assertion depends on content/value/unknown@9']]

## `M05-is_num_const-accepts-bool` — constant / known-value check

- mutation: is_num_const() drops the 'not bool' guard (Constant-value check weakened)
- mutated site executes **4 times** over the three corpora (in 3 cases)
- **structurally equivalent** (not a coverage gap): assign_name() tests is_bool_const(vnode) FIRST (elif chain), so is_num_const() never sees a bool; the mutant's removed guard is unreachable
- **no witness found**: no source in the corpus (or in the fuzzer's grid) separates the pristine from the mutant. This mutant is an equivalent mutant on everything measured.

## `M10-cmp-count-not-flagged` — comparison

- mutation: a count comparison (len(...) == 3) is not a clause-2 violation
- mutated site executes **35 times** over the three corpora (in 28 cases)
- the case that should have killed it — **REASON only**: a count compared for equality inside an assertion

```python
def test_f(): assert len(os.listdir(D)) == 3
```

  - pristine: `{'test_f': 'P0'}` reasons [['count/size comparison (a count is a value, not a path state)@6', 'assertion depends on content/value/unknown@6']]
  - mutant:   `{'test_f': 'P0'}` reasons [['assertion depends on no path state (constant/computed value)@6']]
- reason-level diffs the class-level detectors cannot see: R1=7 selftest cases, R2=6 adversarial cases, R3=4 population ids

## `M13-record-assert-unknown-ok` — assertion

- mutation: an assertion depending on content/value/unknown is not a violation
- mutated site executes **2852 times** over the three corpora (in 379 cases)
- the case that should have killed it — **REASON only**: an assertion whose only dependency is an unknown value

```python
def test_f():
    x = json.loads('{}')['k']
    assert x
```

  - pristine: `{'test_f': 'P0'}` reasons [['call into json.loads (not a plain existence predicate)@7', 'assertion depends on content/value/unknown@8']]
  - mutant:   `{'test_f': 'P0'}` reasons [['call into json.loads (not a plain existence predicate)@7']]
- reason-level diffs the class-level detectors cannot see: R1=26 selftest cases, R2=52 adversarial cases, R3=229 population ids

## `M14-unconditional-fail-ok` — assertion

- mutation: an unconditional / constant-guarded failure is not a violation
- mutated site executes **174 times** over the three corpora (in 83 cases)
- the case that should have killed it — **REASON only**: an unconditional pytest.fail

```python
def test_f():
    pytest.fail('no')
```

  - pristine: `{'test_f': 'P0'}` reasons [['unconditional or constant-guarded failure@7']]
  - mutant:   `{'test_f': 'P0'}` reasons [['no assertion reached that tests path existence']]
- reason-level diffs the class-level detectors cannot see: R1=2 selftest cases, R2=2 adversarial cases, R3=29 population ids

## `M18-if-exit-guard-without-exits` — control flow

- mutation: the 'if <exists>: return' exit guard is set even when the block does not exit
- mutated site executes **56 times** over the three corpora (in 26 cases)
- the case that should have killed it — **CLASS moves**: an 'if <exists>:' block that does NOT exit, followed by an unconditional fail

```python
def test_f():
    if os.path.exists(OUT):
        pass
    pytest.fail('no')
```

  - pristine: `{'test_f': 'P0'}` reasons [['unconditional or constant-guarded failure@9']]
  - mutant:   `{'test_f': 'P1'}` reasons [[]]
- reason-level diffs the class-level detectors cannot see: R1=0 selftest cases, R2=0 adversarial cases, R3=5 population ids

## `M19-for-break-guard-any` — control flow

- mutation: a break guard is honoured even when the condition is not path state
- mutated site executes **27 times** over the three corpora (in 10 cases)
- the case that should have killed it — **REASON only**: fuzzer grid 

```python
def test_f():
    for f in os.listdir(D):
        if len(f) == 1:
            break
    else:
        pytest.fail('never')
```

  - pristine: `{'test_f': 'P0'}` reasons [['count/size comparison (a count is a value, not a path state)@8', 'branch on unknown/content value@8']]
  - mutant:   `{'test_f': 'P0'}` reasons [['count/size comparison (a count is a value, not a path state)@8', 'branch on unknown/content value@8']]

## `M21-async-fixture-not-scanned` — async vs sync

- mutation: Module._scan drops AsyncFunctionDef: an async fixture is not registered
- mutated site executes **2486 times** over the three corpora (in 476 cases)
- the case that should have killed it — **REASON only**: an async fixture that builds a deliverable

```python
import asyncio
@pytest.fixture
async def built():
    subprocess.run(['make'], check=True)
    return Path(OUT)
def test_f(built): assert built.is_file()
```

  - pristine: `{'test_f': 'P0'}` reasons [['call into subprocess.run (not a plain existence predicate)@9']]
  - mutant:   `{'test_f': 'P0'}` reasons [['.is_file() on an unknown/content value@11', 'assertion depends on content/value/unknown@11']]

## `M22-async-test-not-a-unit` — async vs sync

- mutation: test_units drops AsyncFunctionDef: an async test is not a test unit
- mutated site executes **1920 times** over the three corpora (in 460 cases)
- the case that should have killed it — **CLASS moves**: an async test function

```python
import asyncio
async def test_f():
    assert os.path.exists(OUT)
```

  - pristine: `{'test_f': 'P1'}` reasons [[]]
  - mutant:   `{}` reasons []

## `M23-decorators-as-body` — decorators

- mutation: a test's decorators are analysed as body statements
- mutated site executes **1980 times** over the three corpora (in 475 cases)
- **structurally equivalent** (not a coverage gap): exec_stmts() dispatches on the statement type; a decorator is an ast.Call/ast.Attribute, not a statement, and Run has no s_Call handler, so a decorator in the body list is silently ignored
- **no witness found**: no source in the corpus (or in the fuzzer's grid) separates the pristine from the mutant. This mutant is an equivalent mutant on everything measured.

## `M24-parametrize-listing-K` — parametrize

- mutation: a listing-valued parametrize argument is a constant instead of a name
- mutated site executes **33 times** over the three corpora (in 16 cases)
- the case that should have killed it — **CLASS moves**: a parametrize whose values are a listing, compared to a name

```python
import pytest
@pytest.mark.parametrize('p', os.listdir(D))
def test_f(p): assert p == 'a'
```

  - pristine: `{'test_f': 'P1'}` reasons [[]]
  - mutant:   `{'test_f': 'P0'}` reasons [['value comparison of computed values@8', 'assertion depends on content/value/unknown@8']]

## `M25-elem-listing-to-K` — element kind

- mutation: the element kind of a listing is a constant instead of a name
- mutated site executes **1080 times** over the three corpora (in 225 cases)
- the case that should have killed it — **REASON only**: a loop over a listing whose element is compared to a name

```python
def test_f():
    for f in os.listdir(D):
        assert f == 'a.txt'
```

  - pristine: `{'test_f': 'P0'}` reasons [['assertion inside a loop over a listing (universal: depends on absence of other entries)@8']]
  - mutant:   `{'test_f': 'P0'}` reasons [['value comparison of computed values@8', 'assertion inside a loop over a listing (universal: depends on absence of other entries)@8']]

## `M29-class-chain-no-inheritance` — helper visit

- mutation: the class chain does not follow base classes (an inherited method is not found)
- mutated site executes **462 times** over the three corpora (in 20 cases)
- the case that should have killed it — **CLASS moves**: a test class inheriting a helper method from a same-file base class

```python
class B:
    def helper(self):
        return Path(OUT)
class T(B):
    def test_a(self):
        assert self.helper().exists()
```

  - pristine: `{'T.test_a': 'P1'}` reasons [[]]
  - mutant:   `{'T.test_a': 'P0'}` reasons [['self.helper(...) not defined in the file@11', '.exists() on an unknown/content value@11', 'assertion depends on content/value/unknown@11']]

## `M31-is_bool_const-any-constant` — constant / known-value check

- mutation: is_bool_const() accepts any Constant as a boolean (the bool-value check is dropped)
- mutated site executes **984 times** over the three corpora (in 125 cases)
- the case that should have killed it — **CLASS moves**: fuzzer grid 

```python
def test_f():
    n = 0
    if os.path.exists(OUT):
        n = 1
    assert n
```

  - pristine: `{'test_f': 'P0'}` reasons [['assertion depends on content/value/unknown@10']]
  - mutant:   `{'test_f': 'P1'}` reasons [[]]

## `M33-known-k-modules-drop-os` — constant / known-value check

- mutation: the 'os' module is not a known-value module
- mutated site executes **101 times** over the three corpora (in 32 cases)
- the case that should have killed it — **CLASS moves**: the 'os' module bound to a name and branched on

```python
def test_f():
    x = os
    if x:
        assert os.path.exists(OUT)
```

  - pristine: `{'test_f': 'P1'}` reasons [[]]
  - mutant:   `{'test_f': 'P0'}` reasons [['branch on unknown/content value@8']]

## `M38-write-count-not-a-count` — write vs read

- mutation: a write that returns a byte count is not a count value
- mutated site executes **120 times** over the three corpora (in 35 cases)
- the case that should have killed it — **REASON only**: fuzzer grid 

```python
def test_f():
    n = Path(OUT).write_text('x')
    assert n == 1
```

  - pristine: `{'test_f': 'P0'}` reasons [['count/size comparison (a count is a value, not a path state)@8', 'assertion depends on content/value/unknown@8']]
  - mutant:   `{'test_f': 'P0'}` reasons [['value comparison of computed values@8', 'assertion depends on content/value/unknown@8']]

## `M39-mutate-drops-var` — write vs read

- mutation: a mutating call does not update the variable it mutates
- mutated site executes **15 times** over the three corpora (in 11 cases)
- the case that should have killed it — **CLASS moves**: a mutated empty list whose element is a listing

```python
def test_f():
    x = []
    x.append(os.listdir(D))
    assert x
```

  - pristine: `{'test_f': 'P1'}` reasons [[]]
  - mutant:   `{'test_f': 'P0'}` reasons [['assertion depends on no path state (constant/computed value)@9']]
- reason-level diffs the class-level detectors cannot see: R1=0 selftest cases, R2=0 adversarial cases, R3=1 population ids

## `M40-class-attr-self-only` — helper visit

- mutation: a class attribute is only read from the exact class, not its chain
- mutated site executes **1 times** over the three corpora (in 1 cases)
- the case that should have killed it — **CLASS moves**: fuzzer grid 

```python
class B:
    p = Path(OUT)
class T(B):
    def test_a(self):
        assert self.p.exists()
```

  - pristine: `{'T.test_a': 'P1'}` reasons [[]]
  - mutant:   `{'T.test_a': 'P0'}` reasons [['.exists() on an unknown/content value@10', 'assertion depends on content/value/unknown@10']]

## `M41-fixture-autouse-dropped` — helper visit

- mutation: an autouse fixture is not run
- mutated site executes **4 times** over the three corpora (in 4 cases)
- the case that should have killed it — **CLASS moves**: fuzzer grid 

```python
import pytest
@pytest.fixture(autouse=True)
def built():
    subprocess.run(['make'], check=True)
def test_f(): assert os.path.exists(OUT)
```

  - pristine: `{'test_f': 'P0'}` reasons [['call into subprocess.run (not a plain existence predicate)@9']]
  - mutant:   `{'test_f': 'P1'}` reasons [[]]
- reason-level diffs the class-level detectors cannot see: R1=0 selftest cases, R2=0 adversarial cases, R3=4 population ids

