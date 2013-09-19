#!bin/python3

#End Dev Only
import sys, argparse
import csv, re

def main(argv):
        inputfile = ''
        outputfile = ''

        file_parser = argparse.ArgumentParser(description='Convert CSV to Redirects')
        file_parser.add_argument('-o', '--output', help='output file for redirects')
        file_parser.add_argument('-i', '--input', help='input CSV file, needs column "url", and column "redirect"')
        file_parser.add_argument('-d', '--domain', help='redirect domain, ie: http://www.google.com')
        args = file_parser.parse_args()

        parsed_redirect = parsecsv(args.input, args.domain)

        write_to_file(parsed_redirect, args.output)

## Parses CSV
def parsecsv(input_file, domain):
        redirects = []

        try:
                with open(input_file, newline='') as csvfile:
                        compete_redirect = ""

                        url_breakdown = DictReaderInsensitive(csvfile, delimiter=',')
                        for row in url_breakdown:
                                redirects.append(row['redirect'])
                                compete_redirect = compete_redirect+generate_redirects(row['url'], row['redirect'].lower(), domain)

                        check_redirects(redirects)

                        print(compete_redirect)
                        return compete_redirect
        except IOError:
                print('Error')

#Confirm redirects
def check_redirects(redirect_array):
        redirect_array.sort()
        #lowercase everything
        redirect_array = [x.lower() for x in redirect_array]
        redirect_array = set(redirect_array)

        redirect_array_string = "\n ".join(redirect_array)
        redirect_string = 'Redirect to these pages:\n-----\n '+redirect_array_string+'\n----\n\n'

#Generate Text redirect
def generate_redirects(redirect_url, redirect, domain):
        #generated_redirects = 'Redirect 301 '+parse_redirect_urls(redirect_url)+' '+generate_url(domain,redirect)+'\n'
        ##
        ##
                ## CHANGE THIS STRING ##
        ##
        ##
        generated_redirects = ''+parse_redirect_urls(redirect_url)+'|'+generate_url(domain,redirect)+'|0|0\n'
        ##
        ##
                ## CHANGE THIS STRING ##
        ##
        ##

        return generated_redirects

#Generate URL for redirect
def generate_url(url, page):
        newurl = url+'/'+page
        return newurl

#Parse out old domains
def parse_redirect_urls(url_to_breakdown):
        match = re.sub("(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))", '', url_to_breakdown)
        return match

##Write to File
def write_to_file(completed_redirects, outputfile):
        try:
                with open(outputfile, "w") as writefile:
                        writefile.write(completed_redirects)
        except IOError:
                print("Error")
#Class Insensitive CSV Reader
class DictReaderInsensitive(csv.DictReader):
    # This class overrides the csv.fieldnames property.
    # All fieldnames are without white space and in lower case

    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(DictReaderInsensitive, self).fieldnames]

    def __next__(self):
        # get the result from the original __next__, but store it in DictInsensitive

        dInsensitive = DictInsensitive()
        dOriginal = super(DictReaderInsensitive, self).__next__()

        # store all pairs from the old dict in the new, custom one
        for key, value in dOriginal.items():
            dInsensitive[key] = value

        return dInsensitive

class DictInsensitive(dict):
    # This class overrides the __getitem__ method to automatically strip() and lower() the input key

    def __getitem__(self, key):
        return dict.__getitem__(self, key.strip().lower())
#End Class Insensitive CSV Reader

#Initialize function main :D
if __name__ == '__main__':
        main(sys.argv[1:])
