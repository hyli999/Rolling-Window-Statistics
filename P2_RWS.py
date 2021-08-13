import csv
import statistics
import seaborn as sns
import matplotlib.pylab as plt


def read_file(filename , date_index , field_index , has_header=True):
    """
    Reads a csv file and parses the content field into a time series.
    Input :
    filename : csv filename
    date_index: zero-based index of the time series date field
    field_index: zero-based index of the time series content field
    has_header : True or False on whether the file contents has a header row Output :
    time_series : list of tuples with tuple consisting of (date , content field )
    """
    time_series = []
    with open(filename) as csvfile :
        reader = csv.reader(csvfile , delimiter=",")
        if has_header :
            next(reader , None)
        for row in reader :
            time_series .append((row[ date_index ] , float(row[ field_index ])))
        return time_series

def main():
    """
    the main function that collects data from the spreadsheet and calculates the key statistics
    """

    # open and read file to populate date and adjusted close
    filename = "GOOG.csv"
    ts = read_file(filename, 0, 5)
    print(f"{filename} has been read with {len(ts)} daily prices ")

    # ask the user to input the window size
    # check whether the window size is valid (If not, ask for a valid input again.)
    window_size = int(input(f"Please enter your preferred window size (Please enter an integer between 2 and {len(ts)}.)"))
    while True:
        if 2<=window_size<=len(ts):
            break
        else:
            window_size = int(input(f"Please enter an integer between 2 and {len(ts)}"))

    # compute the key rolling statistics including mean, median, max, min, and standard deviation from each time period
    mean, median, high, low, SD = [], [], [], [], []
    earliest_date = 0
    for last_date in range (window_size, len(ts)):
        date_range = ts[earliest_date:last_date]
        #get the mean
        mean.append((date_range[-1][0], statistics.mean([date_range[i][1] for i in range(window_size)])))
        #get the median
        median.append((date_range[-1][0], statistics.median([date_range[i][1] for i in range(window_size)])))
        #get the highest stock price
        high.append((date_range[-1][0], max([date_range[i][1] for i in range(window_size)])))
        #get the lowest stock price
        low.append((date_range[-1][0], min([date_range[i][1] for i in range(window_size)])))
        #get the standard deviation
        SD.append((date_range[-1][0], statistics.stdev([date_range[i][1] for i in range (window_size)])))
        #go to the next period, and run the loop again
        earliest_date += 1

    # plot the key statistics onto the graph together with the adjusted closing price
    sns.set()
    fig, ax = plt.subplots()
    #plot the adjusted closing price using color black
    ax.plot([ts[i][0] for i in range (len(ts))], [ts[i][1] for i in range (len(ts))], linewidth = 2, label = "Adjusted Close", color = "black")
    #plot the maximum price using color yellow
    ax.plot([high[i][0] for i in range(len(high))], [high[i][1] for i in range(len(high))], linewidth=2, label="Maximum",
            color="yellow")
    #plot the minimum price using color yellow
    ax.plot([low[i][0] for i in range(len(low))], [low[i][1] for i in range(len(low))], linewidth=2, label="Minimum",
            color="yellow")
    #plot the median using color green
    ax.plot([median[i][0] for i in range(len(median))], [median[i][1] for i in range(len(median))], linewidth=2, label="Median",
            color="green")
    #plot the mean using color red
    ax.plot([mean[i][0] for i in range(len(mean))], [mean[i][1] for i in range(len(mean))], linewidth=2, label="Mean",
            color="red")
    #plot the graph of 2 standard deviations from the mean using color purple
    ax.plot([SD[i][0] for i in range(len(SD))], [mean[i][1] + 2*SD[i][1] for i in range(len(SD))], linewidth=2, label="Mean + 2 Standard Deviations",
            color="purple")
    ax.plot([SD[i][0] for i in range(len(SD))], [mean[i][1] - 2*SD[i][1] for i in range(len(SD))], linewidth=2,
            label="Mean - 2 Standard Deviations",
            color="purple")
    #standardize the axis and title, and draw the graph
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")
    ax.set_title(f"{window_size}-day Rolling Statistics for Google Using Adjusted Closing Price")
    ax.legend(loc = "best", fontsize = "x-small")
    plt.show()


#run the function
if __name__ == "__main__":
    main()
