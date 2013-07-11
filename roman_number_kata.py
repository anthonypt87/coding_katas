"""Convert roman numerals to values http://codingdojo.org/cgi-bin/wiki.pl?KataRomanNumerals."""

numeral_to_values = {
	'I': 1,
	'V': 5,
	'X': 10,
	'L': 50,
	'C': 100,
}


def roman_to_value(roman_number_string):
	value = 0
	for position in range(len(roman_number_string)):
		value_of_current_character = _get_value_of_character_at_position(roman_number_string, position)

		if position + 1 >= len(roman_number_string):
			value += value_of_current_character
			continue

		value_of_next_character = _get_value_of_character_at_position(roman_number_string, position + 1)

		if value_of_next_character > value_of_current_character:
			value -= value_of_current_character
		else:
			value += value_of_current_character

	return value


def _get_value_of_character_at_position(roman_number_string, position):
		current_character = roman_number_string[position]
		return numeral_to_values[current_character]


if __name__ == '__main__':
	assert roman_to_value('I') == 1
	assert roman_to_value('II') == 2
	assert roman_to_value('III') == 3
	assert roman_to_value('IV') == 4, roman_to_value('IV')
	assert roman_to_value('V') == 5
	assert roman_to_value('VI') == 6
	assert roman_to_value('XVIII') == 18
	assert roman_to_value('XXIV') == 24
	assert roman_to_value('XCIV') == 94
