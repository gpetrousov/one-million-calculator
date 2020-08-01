import sys
import argparse
from tabulate import tabulate
from datetime import datetime
import csv


YEARLY_SEPARATOR = "#==========#"


def find_starting_month():
    """Returns an integer which shows the current month"""
    today = datetime.today()
    current_month = today.month
    return current_month

def find_starting_year():
    """Returns an integer which shows the current year"""
    today = datetime.today()
    current_year = today.year
    return current_year


def write_results_into_csv(field_names, data_to_write):

    with open("simulation_results.csv", mode="w") as results_file:
        csv_results_writer = csv.writer(results_file)
        csv_results_writer.writerow(field_names)
        csv_results_writer.writerows(data_to_write)

    return


def main(monthly_input, annual_increase, annual_percentage_growth, amount_of_years, results_detail="mo", starting_amount=0):

    total_investment_value = starting_amount # How much the investments are worth
    total_amount_invested = starting_amount # How much was invested so far, just a sum
    investments_returns = 0 # How much money is returned by the investments: =(total_investment_value-total_amount_invested)
    annual_input = monthly_input * 12
    monthly_percentage_growth = float(annual_percentage_growth/12)

    annual_simulation_table_headers = ["Year", "Yearly input", "Total amount invested", "Total investment value", "Investment returns"]
    monthly_simulation_table_headers = ["Date (Month/Year)", "Monthly input", "Total amount invested", "Total investment value", "Investment returns"]

    simulation_table = []

    starting_month = find_starting_month()
    starting_year = find_starting_year()
 
    if results_detail == "mo":
        for year in range(starting_year, starting_year+amount_of_years):
            for month in range(starting_month, 13):
                total_amount_invested += monthly_input

                total_investment_value +=  monthly_input
                total_investment_value += total_investment_value * monthly_percentage_growth

                investments_returns = total_investment_value - total_amount_invested

                end_date = "{}/{}".format(month, year)
                simulation_table.append([end_date, monthly_input, total_amount_invested, round(total_investment_value, 2),  round(investments_returns, 2)])

            starting_month = 1
            simulation_table.append([YEARLY_SEPARATOR, YEARLY_SEPARATOR, YEARLY_SEPARATOR, YEARLY_SEPARATOR])
            monthly_input += monthly_input * annual_increase

        print(tabulate(simulation_table, headers=monthly_simulation_table_headers, tablefmt="fancy_grid", floatfmt=".2f"))
        write_results_into_csv(monthly_simulation_table_headers, simulation_table)

    elif results_detail == "ye":
        for year in range(starting_year, starting_year+amount_of_years):
            total_amount_invested += annual_input

            total_investment_value +=  annual_input
            total_investment_value += total_investment_value * annual_percentage_growth

            investments_returns = total_investment_value - total_amount_invested

            simulation_table.append([year, annual_input, total_amount_invested, round(total_investment_value, 2),  round(investments_returns, 2)])

            annual_input += annual_input * annual_increase

        print(tabulate(simulation_table, headers=annual_simulation_table_headers, tablefmt="fancy_grid", floatfmt=".2f"))
        write_results_into_csv(annual_simulation_table_headers, simulation_table)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()                                                                                                                                               

    parser.add_argument("-s", "--starting_amount", type=int, required=True, help="The amount we have already invested.")
    parser.add_argument("-mi", "--monthly_input",  type=int, required=True, help="The amount that we put into our investments every month.")
    parser.add_argument("-ai", "--annual_increase", type=float, required=True, help="The percent that we incrase our monthly input each year.")
    parser.add_argument("-r", "--annual_percentage_growth", type=float, required=True, help="The percent that our investments rise in value at the end of the year.")
    parser.add_argument("-y", "--amount_of_years", type=int, required=True, help="The amount of years to simulate for.")
    parser.add_argument("-d", "--detail", type=str, required=False, default="mo", help="mo: Monthly calculations || ye: Yearly calculations")
    args = parser.parse_args()
    main(args.monthly_input, args.annual_increase/100, args.annual_percentage_growth/100, args.amount_of_years, results_detail=args.detail, starting_amount=args.starting_amount)

