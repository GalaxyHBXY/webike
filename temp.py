# import stripe
# stripe.api_key = "sk_test_51LgjMIBRIrkzup4Hpb3Djfs7PkRr45MfJNTIv0up4c80e1yEcAFWUyZA4HQ7EhuKOJzPFlohMnJP3EE7xbDp0XZX00NVPf9fer"
#
# a = stripe.checkout.Session.retrieve(
#   # "cs_test_a1NP8LXHiR7ZL1BBEB9xSsRzrBUUf7VILLvsFcxaCpXGe7zwPkqCa9e66U",
#   "cs_test_a1YMKhjIMaiUIrqW3MdXw8F9PHzMZPmVT8vFrsvLTxDCMtdiKq3asfuPRX"
# )
#
# # print(a["subscription"])
#
# print(a)

def main():
  a = {"a":1,"b":2}
  a["c"]=3

  print(a)

if __name__ == '__main__':
    main()
