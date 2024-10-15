from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import pickle
 
 
 
class ChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("Easy Flow Pie Chart")
        self.setGeometry(100,100, 1600,900)
 
        
 
        self.create_piechart()
        self.show()
 
 
    def create_piechart(self):
 
        with open('array_data.pkl', 'rb') as f:
            cost_array = pickle.load(f)

        print("Loaded array in other script:")
        print(cost_array)

        print(cost_array[0][1])    
        names = [item[0] for item in cost_array]  # First elements (labels)
        values = [item[1] for item in cost_array]  # Second elements (values)

        print(names)
        print(values)

        series = QPieSeries()
        series.append(names[0], values[0])
        series.append(names[1], values[1])
        series.append(names[2], values[2])
        series.append(names[3], values[3])
        series.append(names[4], values[4])
        series.append(names[5], values[5])
        series.append(names[6], values[6])
        series.append(names[7], values[7])
        series.append(names[8], values[8])
        series.append(names[9], values[9])
        series.append(names[10], values[10])
        series.append(names[11], values[11])
        series.append(names[12], values[12])
        series.append(names[13], values[13])

        i = 0
        max_value = max(values)  # Store the maximum value
        found = False  # Flag to indicate if the max value has been found
        max_index = ""

        while not found and i < len(values):  # Loop until the max value is found or i exceeds the length
            if values[i] == max_value:
                print(i)  # Print the index of the maximum value
                found = True  # Set found to True to exit the loop
                max_index = i
            i += 1  # Increment i

        #adding slice
        slice = QPieSlice()
        slice = series.slices()[int(max_index)]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(Qt.darkGreen, 2))
        slice.setBrush(Qt.green)
 
 
 
 
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Monthly Costs")
 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
 
        self.setCentralWidget(chartview)
 
 
 
 
 
App = QApplication(sys.argv)
window = ChartApp()
sys.exit(App.exec_())