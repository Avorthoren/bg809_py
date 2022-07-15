import dataclasses
import itertools
import time
from typing import Iterable

N = 12
_MOVES_V = -2, -2, -1, -1,  1, 1,  2, 2
_MOVES_H = -1,  1, -2,  2, -2, 2, -1, 1


@dataclasses.dataclass(slots=True)
class Position:
	v: int
	h: int

	def attacks(self, pos: "Position"):
		return self.v == pos.v or self.h == pos.h

	def is_inside(self, n: int = N) -> bool:
		return 0 <= self.v < n and 0 <= self.h < n

	def all_horse_moves(self, n: int = N) -> Iterable["Position"]:
		"""Yields self as results of all horse moves from initial self position.
		Mutates self.
		"""
		# Store self initial position.
		v, h = self.v, self.h
		for dv, dh in zip(_MOVES_V, _MOVES_H):
			self.v, self.h = v + dv, h + dh
			if self.is_inside(n):
				yield self
		# Restore self initial position.
		self.v, self.h = v, h


Perm_T = tuple[Position, ...]


def check(rooks_perm: Perm_T, n: int = N, i: int = 0) -> bool:
	"""Check if each rook of `rooks_perm` from i-th to last can be moved
	with horse move such that neither rook attacks any other.
	"""
	for pos in rooks_perm[i].all_horse_moves(n):
		bad_try = False
		for j in range(i):
			if pos.attacks(rooks_perm[j]):
				bad_try = True
				break
		if bad_try:
			continue

		if i == n-1 or check(rooks_perm, n, i+1):
			return True

	return False


def rooks_perm_to_str(rooks_perm: Perm_T) -> str:
	return " ".join(f"({rp.v}, {rp.h})" for rp in rooks_perm)


def rooks_permutations(n: int = N, k: int = None) -> Iterable[Perm_T]:
	"""Yields all permutation of k rooks on nxn field such that neither rook
	attacks any other.
	Vertical position of leftmost rook will be at most n/2 to exclude
	obvious symmetric variants.
	"""
	if k is None:
		k = n

	rooks_perm = tuple(Position(0, 0) for _ in range(k))

	for vs in itertools.combinations(range(n), k):
		max_first_index = (n - 1) >> 1
		for hs in itertools.permutations(range(n), k):
			if hs[0] > max_first_index:
				break

			for i, (v, h) in enumerate(zip(vs, hs)):
				p = rooks_perm[i]
				p.v, p.h = v, h

			yield rooks_perm


def search_bad_perm(n: int = N, k: int = None) -> Perm_T | None:
	"""Search permutation of k rooks on nxn field (such that neither rook
	attacks any other) such it is not possible to move each rook with horse
	move, so that neither rook attacks any other.
	"""
	if k is None:
		k = n

	MAX_CNT = 10_000
	cnt = 0
	for i, rooks_perm in enumerate(rooks_permutations(n, k)):
		cnt += 1
		if cnt == MAX_CNT:
			cnt = 0
			print(f"{i+1: 10}: {rooks_perm_to_str(rooks_perm)}")

		if not check(rooks_perm, n):
			return rooks_perm

	return None


def main():
	t0 = time.perf_counter()
	bad_perm = search_bad_perm(12)
	t1 = time.perf_counter()

	if bad_perm is None:
		print("SUCCESS!")
	else:
		print("BAD PERMUTATION FOUND:")
		print(rooks_perm_to_str(bad_perm))

	print(f"{t1 - t0} s")


if __name__ == "__main__":
	main()

