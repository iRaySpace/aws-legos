import argparse
import dns.resolver


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    args = parser.parse_args()

    try:
        records = dns.resolver.resolve(args.domain, 'TXT')
        for record in records:
            print("::> " + str(record))
    except Exception as e:
        print("ERR::> Please check your internet or your domain")
