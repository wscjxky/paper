import re
url='https://www.researchgate.net/publication/319362128_Channel_Estimation_with_Expectation_Maximization_and_Historical_Information_based_Basis_Expansion_Model_for_Wireless_Communication_Systems_on_High_Speed_Railways'
print(re.search('\d+_(.+)',url).group(1))