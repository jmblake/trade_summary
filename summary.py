import csv
import pandas as pd


class Summary:
    """
    Accepts csv file of trades and outputs a csv file of instrument trade 
    summaries.
    """
    
    def __init__(self, in_path, out_path):
        """
        Parameters
        ----------
        in_path: str
            File of trades.
            Columns are: 'Time Stamp', 'Symbol', 'Quantity', 'Price'.
        out_path: str
            File with trade summaries ordered alphabetically by instrument.
            Columns are: 'Symbol', 'Maximum Time Gap', 'Volume', 
            'Weighted Average Price', 'Maximum Price'.
        """

        # Initialise the in and out paths
        self.in_path = in_path
        self.out_path = out_path

        # Initialise the trade data
        self.trade_data = None

        # Initialise the summary dictionary
        self.trade_summary = {}

        # Initialise the output DataFrame
        self.df = None

    def load_trade_data(self):
        """
        Load the trade data
        """
        file = open(self.in_path)
        trade_data = csv.reader(file)

        return trade_data

    @staticmethod
    def parse_row_details(row):
        """
        Parse a row
        """
        time_stamp = int(row[0])
        symbol = row[1]
        quantity = int(row[2])
        price = int(row[3])

        return time_stamp, symbol, quantity, price

    def update_symbol_details(self, row):
        """
        Update the symbol details based on the row
        """
        time_stamp, symbol, quantity, price = self.parse_row_details(row)
        if symbol == '':
            raise ValueError('Symbol data missing')
        if symbol not in self.trade_summary:
            # If the dictionary does not yet contain any data for trades on the
            # given symbol, we populate the dictionary with a list of relevant 
            # data that we will update to eventually produce our summary.
            max_gap = 0
            total_quantity = quantity
            max_price = price
            total_price = quantity*price
        else:
            old_summary = self.trade_summary.get(symbol).copy()
            # If the dictionary already contains an entry for the given symbol,
            # we implement the following replacement scheme:
            max_gap = max(time_stamp - old_summary['time_stamp'], 
                          old_summary['max_gap'])
            total_quantity = quantity + old_summary['volume']
            max_price = max(price, old_summary['max_price'])
            total_price = price * quantity + old_summary['total_price']

        self.trade_summary[symbol] = {'time_stamp': time_stamp,
                                      'max_gap': max_gap,
                                      'volume': total_quantity,
                                      'max_price': max_price,
                                      'total_price': total_price}

    def trade_summary_to_df(self):
        """
        Convert the trade summary dictionary to a DataFrame
        """
        # Passing the dictionary of dictionaries to a DataFrame, then 
        # transposing to get symbols as row headings.
        df = pd.DataFrame(self.trade_summary).T

        # Sorting the DataFrame rows by symbol, ascending.
        df.sort_index(inplace=True)

        # We add another column, which gives the average price for each symbol.
        df['av_price'] = df.apply(lambda row: row.total_price // row.volume, axis=1)

        # Now, finally we remove some columns, and swap the position of the 
        # 'max_price' and 'av_price' columns.
        column_order = ['max_gap', 'volume', 'av_price', 'max_price']
        df = df.reindex(columns=column_order)

        return df

    def save_df(self, out_path):
        """
        Save the DataFrame to a csv file
        """
        # In keeping with the formatting of the input csv file, we don't 
        # include column headings.
        self.df.to_csv(path_or_buf=out_path, header=False)

    def run(self):
        """
        Parse through the input data, create an output df and save to file
        """
        self.trade_data = self.load_trade_data()
        for row in self.trade_data:
            self.update_symbol_details(row)
        self.df = self.trade_summary_to_df()
        self.save_df(self.out_path)


def main():
    in_path = './data/input.csv'
    out_path = './data/output.csv'

    Summary(in_path, out_path).run()


if __name__ == '__main__':
    main()
