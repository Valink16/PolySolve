from re import sub, split, finditer, search

class Poly:
	def __init__(self, coefficients: dict):
		self.coefficients = coefficients

	def __repr__(self):
		s = ""
		for k in self.coefficients:
			s += '+' if self.coefficients[k] > 0 else ''
			if k == 0:
				s += str(self.coefficients[k])
			elif k == 1:
				s += (str(self.coefficients[k]) if not self.coefficients[k] == 1 else '') + 'x'
			else:
				s += "{}x^{}".format((str(self.coefficients[k]) if not self.coefficients[k] == 1 else ''), k)

		if s.startswith('+'):
			s = s[1:]

		return s if len(s) > 0 else '0'

	def __sub__(self, other):
		current = dict(self.coefficients)
		for k in other.coefficients:
			if k in current:
				current[k] -= other.coefficients[k]
				if current[k] == 0:
					current.pop(k)
			else:
				current[k] = -other.coefficients[k]
		return Poly(current)

	def __floordiv__(self, other):
		other_degrees = list(other.coefficients.keys())
		other_degrees.sort()

		other_first_m_deg = other_degrees[len(other_degrees) - 1]
		other_first_m_coeff = other.coefficients[other_first_m_deg]

		remaining = Poly(self.coefficients) # Keep track of the remaining coefficients

		res_coefficients = dict()

		while not len(remaining.coefficients) == 0:
			# Pick the member with the biggest degree
			keys = list(remaining.coefficients.keys())
			keys.sort()
			rem_first_deg = keys[len(keys) - 1]

			# Checking if the reminder can still be devided
			if rem_first_deg - other_first_m_deg >= 0 and remaining.coefficients[rem_first_deg] % other_first_m_coeff == 0:
				# Dividing using power properties
				new_deg = rem_first_deg - other_first_m_deg
				new_coeff = remaining.coefficients[rem_first_deg] // other_first_m_coeff
			else:
				break

			sub = other * Poly( {new_deg: new_coeff} ) # The value to reduce from the remaining
			remaining -= sub

			res_coefficients[new_deg] = new_coeff
		return Poly(res_coefficients)

	def __mod__(self, other):
		other_degrees = list(other.coefficients.keys())
		other_degrees.sort()

		other_first_m_deg = other_degrees[len(other_degrees) - 1]
		other_first_m_coeff = other.coefficients[other_first_m_deg]

		remaining = Poly(self.coefficients) # Keep track of the remaining coefficients

		while not len(remaining.coefficients) == 0:
			# Pick the member with the biggest degree
			keys = list(remaining.coefficients.keys())
			keys.sort()
			rem_first_deg = keys[len(keys) - 1]

			# Checking if the reminder can still be devided
			if rem_first_deg - other_first_m_deg >= 0 and remaining.coefficients[rem_first_deg] % other_first_m_coeff == 0:
				# Dividing using power properties
				new_deg = rem_first_deg - other_first_m_deg
				new_coeff = remaining.coefficients[rem_first_deg] // other_first_m_coeff
			else:
				break

			sub = other * Poly( {new_deg: new_coeff} ) # The value to reduce from the remaining
			remaining -= sub
		return remaining
	
	def __mul__(self, other):
		coeffs = dict()
		for deg_1 in self.coefficients:
			
			for deg_2 in other.coefficients:
				deg = deg_1 + deg_2
				coeff = self.coefficients[deg_1] * other.coefficients[deg_2]
				if deg in coeffs: # Simplify same degree members
					coeffs[deg] += coeff
				else:
					coeffs[deg] = coeff
		return Poly(coeffs)

	@classmethod
	def from_str(cls, s: str):
		s = sub(r'\s+', '', s) # Using regex to remove all spaces

		# Using regex to extract each member of the polynomial
		match_pattern = r'[\-\+]?(([0-9]*)+x?(\^[0-9]+)?)'
		members = [s[m.start():m.end()] for m in finditer(match_pattern, s)]
		members.remove('') # Removing the last match which is somehow always empty

		coefficients = dict()
		for m in members:
			if m.startswith('+'): # Removing useless + sign
				m = m[1:]

			# Getting the coeffcient in front of x
			if 'x' in m: # Exception for degree 0 members
				if m.startswith('-'):
					coeff = -1 if m.startswith('-x') else int(m.split('x')[0])
				else:
					coeff = 1 if m.startswith('x') else int(m.split('x')[0])
			else:
				coeff = int(m)

			# Getting the degree of the member
			m_deg = search(r'(?<=\^)[0-9]+', m)
			if m_deg == None: # If the degree is not specified
				m_deg = 1 if 'x' in m else 0 # The member can be either degree 0 or 1, (0 if it's the y intercept, so no x with it)
			else:
				m_deg = int(m[m_deg.start():m_deg.end()]) 

			coefficients[m_deg] = coeff # Populate the dict
		return cls(coefficients)
	
	# Returns computed image for preimage
	def image(self, preimage):
		img = 0
		for k in self.coefficients.keys():
			img += preimage ** k * self.coefficients[k]
		return img

	# Returns the degree of the polynomial
	def degree(self):
		return max(list(self.coefficients.keys()))

	# Returns if the polynomial is a null value(a constant 0)
	def is_zero(self):
		return len(self.coefficients) == 0

	# Returns every roots of the polynomial
	def roots(self):
		pass