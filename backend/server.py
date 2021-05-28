from flask import Flask, jsonify, request
import json
import requests
import unittest

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = 'dev'


######################### API ROUTES/ENDPOINTS #########################


@app.route('/api/prices', methods=['GET'])
def get_insurance_prices():
    term = request.args.get('term')
    coverage = request.args.get('coverage_amount')
    
    try:
        premiums = get_lowest_premiums()
    except:
        premiums = API_LOWEST_PRICES

    terms = sorted(list(set([t for t, c in premiums])))
    coverages = sorted(list(set([c for t, c in premiums])))
    
    adj_terms = get_adjacent_nums(terms, int(term))
    adj_coverages = get_adjacent_nums(coverages, int(coverage))
        
    results = [{**{str(t): premiums.get((t, c)) for t in adj_terms}, **{'coverage':c}} for c in adj_coverages]

    return jsonify({'terms': adj_terms,
                    'coverages': adj_coverages, 
                    'prices': results})


########################### HELPER FUNCTIONS ###########################


def get_adjacent_nums(nums, num):
    nums.sort()
    i = nums.index(num) 

    if num == nums[0]: return nums[:3]
    elif num == nums[-1]: return nums[-3:]
    else: return nums[i-1:i+2]


def get_lowest_premium(data):
    premiums = {}
    return sorted([prem['premium']for prem in data['policies']])[0]


def get_lowest_premiums():
    results = {}
    terms = [10, 15, 20, 25, 30]
    coverages = [100000, 250000, 500000, 1000000, 5000000, 10000000]

    for term in terms:
        for coverage in coverages:
            response = requests.get(f'http://5be45b4482db.ngrok.io/policies?term={term}&coverage_amount={coverage}')
            data = json.loads(response.text)
            if data['policies']:
                results.setdefault((term, coverage), get_lowest_premium(data))
            
    return results


################################ TESTS #################################


TEST_DATA = {"policies": [{"premium":8.62,"carrier":"Good insurance"},
                          {"premium":9.54,"carrier":"Geico"},
                          {"premium":8.24,"carrier":"Uncle Bob's Insurance Shack"},
                          {"premium":7.19,"carrier":"Insurance 4 U"}]}

TEST_NUMS = [4, 10, 1, 500, 3] 

API_LOWEST_PRICES = {(10, 100000): 5.1, 
                     (10, 250000): 15.96, 
                     (10, 500000): 24.18, 
                     (10, 1000000): 50.31, 
                     (10, 5000000): 232.3, 
                     (15, 100000): 4.59, 
                     (15, 250000): 13.58, 
                     (15, 500000): 31.38, 
                     (15, 1000000): 47.43, 
                     (15, 5000000): 174.97, 
                     (15, 10000000): 641.48, 
                     (20, 100000): 5.96, 
                     (20, 250000): 14.7, 
                     (20, 500000): 19.49, 
                     (20, 1000000): 68.45, 
                     (20, 5000000): 314.09, 
                     (20, 10000000): 644.17, 
                     (25, 100000): 7.86, 
                     (25, 250000): 18.51, 
                     (25, 500000): 41.05, 
                     (25, 1000000): 63.85, 
                     (25, 5000000): 251.2, 
                     (25, 10000000): 776.32, 
                     (30, 100000): 7.19, 
                     (30, 250000): 17.59, 
                     (30, 500000): 44.66, 
                     (30, 1000000): 60.09, 
                     (30, 5000000): 350.67, 
                     (30, 10000000): 698.87}


class TestGetLowestPremium(unittest.TestCase):
    def test_get_lowest_premium(self):
        actual = get_lowest_premium(TEST_DATA)
        expected = 7.19
        self.assertEqual(actual, expected)


class TestGetAdjacentNums(unittest.TestCase):
    def test_adjacent_nums(self):
        actual = get_adjacent_nums(TEST_NUMS, 4)
        expected = [3, 4, 10]
        self.assertEqual(actual, expected)

    def test_lowest_adjacent_nums(self):
        actual = get_adjacent_nums(TEST_NUMS, 1)
        expected = [1, 3, 4]
        self.assertEqual(actual, expected)
    
    def test_highest_adjacent_nums(self):
        actual = get_adjacent_nums(TEST_NUMS, 500)
        expected = [4, 10, 500]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    # connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    unittest.main()
    