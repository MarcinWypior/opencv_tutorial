input_string = "AB_ETHIP-1\\{DUT_ADAPTER_1_IP_ADDRESS}\\Backplane\\0"
FSSI_NR = 2

# Replace the last '0' after the last backslash '\' with 'word'
new_string = input_string.rsplit('\\', 1)
new_string = f"{new_string[0]}\\{FSSI_NR}"

print(new_string)
print(input_string)