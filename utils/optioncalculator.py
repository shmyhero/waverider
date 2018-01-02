import math
import numpy as np
import vollib.black_scholes
import vollib.black_scholes.implied_volatility
import vollib.black_scholes_merton
import vollib.black_scholes_merton.implied_volatility
import vollib.black_scholes.greeks.numerical


class OptionCalculator(object):

    @staticmethod
    def get_history_volatility(price_list):
        X = []
        for i in range(len(price_list)-2):
            X.append(math.log(price_list[i+1]/price_list[i]))
            #X.append((price_list[i + 1] - price_list[i])/price_list[i])
        #print X
        return np.std(X)

    @staticmethod
    def get_history_volatility2(price_list):
        dailyVolatility = np.std(np.diff(np.log(price_list)))
        return dailyVolatility

    @staticmethod
    def get_year_history_volatility(price_list):
        return math.sqrt(252) * OptionCalculator.get_history_volatility2(price_list)

    @staticmethod
    def get_year_history_volatility_list(date_price_records, circle = 30):
        length = len(date_price_records)
        results = []
        for i in range(length-circle):
            price_list = map(lambda x: x[1], date_price_records[i:i+circle])
            vol = OptionCalculator.get_year_history_volatility(price_list)
            results.append([date_price_records[i+circle][0], vol])
        return results

    @staticmethod
    def get_black_scholes_option_price(underlying_price, strike_price, days_to_experiation, risk_free_interest_rate, sigma, flag='c'):
        price = vollib.black_scholes.black_scholes(flag, underlying_price, strike_price, days_to_experiation, risk_free_interest_rate, sigma)
        return price

    @staticmethod
    def get_implied_volatility(current_price, underlying_price, strike_price, left_days, interest_rate, flag='c'):
        return vollib.black_scholes.implied_volatility.implied_volatility(current_price, underlying_price, strike_price,
                                                                   left_days / 365.0, interest_rate, flag)

    @staticmethod
    def get_delta(underlying_price, strike_price, left_days, risk_free_interest_rate, sigma, flag='c'):
        delta = vollib.black_scholes.greeks.numerical.delta(flag, underlying_price, strike_price, left_days/365.0, risk_free_interest_rate, sigma)
        return delta

    @staticmethod
    def get_gamma(underlying_price, strike_price, left_days, risk_free_interest_rate, sigma, flag='c'):
        gamma = vollib.black_scholes.greeks.numerical.gamma(flag, underlying_price, strike_price, left_days/365.0, risk_free_interest_rate, sigma)
        return gamma

    @staticmethod
    def get_vega(underlying_price, strike_price, left_days, risk_free_interest_rate, sigma, flag='c'):
        vega = vollib.black_scholes.greeks.numerical.vega(flag, underlying_price, strike_price, left_days/365.0, risk_free_interest_rate, sigma)
        return vega

    @staticmethod
    def get_theta(underlying_price, strike_price, left_days, risk_free_interest_rate, sigma, flag='c'):
        theta = vollib.black_scholes.greeks.numerical.theta(flag, underlying_price, strike_price, left_days/365.0, risk_free_interest_rate, sigma)
        return theta

    @staticmethod
    def get_rho(underlying_price, strike_price, left_days, risk_free_interest_rate, sigma, flag='c'):
        rho = vollib.black_scholes.greeks.numerical.rho(flag, underlying_price, strike_price, left_days/365.0, risk_free_interest_rate, sigma)
        return rho

if __name__ == '__main__':
    import datetime
    from dataaccess.db import YahooEquityDAO
    from_date_str = (datetime.date.today() - datetime.timedelta(100)).strftime('%Y-%m-%d')
    equity_records = YahooEquityDAO().get_all_equity_price_by_symbol('SPY', from_date_str)
    results = OptionCalculator.get_year_history_volatility_list(equity_records)
    print results

