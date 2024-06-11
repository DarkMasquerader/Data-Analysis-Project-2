def generate_if_statement(field_names):
    if len(field_names) < 2:
        raise ValueError("At least two field names are required to generate the IF statement.")

    # Start with the first comparison
    if_statement = f'IF [{field_names[0]}] >= [{field_names[1]}] AND ' + ' AND '.join([f'[{field_names[0]}] >= [{field}]' for field in field_names[2:]]) + f' THEN "{field_names[0]}"\n'

    # Loop through the rest of the fields and add ELSEIF conditions
    for i in range(1, len(field_names)):
        other_fields = [field for j, field in enumerate(field_names) if j != i]
        elseif_condition = f'ELSEIF [{field_names[i]}] >= [{other_fields[0]}] AND ' + ' AND '.join([f'[{field_names[i]} >= [{field}]' for field in other_fields[1:]]) + f' THEN "{field_names[i]}"\n'
        if_statement += elseif_condition

    # End statement
    if_statement += f'END'

    return if_statement

# Example usage:
field_names = [
    'No. Associate Level',
    'No. Director Level',
    'No. Entry Level',
    'No. Internship Level',
    'No. Mid-Senior Level',
]

if_statement = generate_if_statement(field_names)
print(if_statement)
