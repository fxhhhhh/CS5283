
import matplotlib.pyplot as plt
if __name__ == '__main__':
    res = []
    f_name = "test1.txt"
    with open(f_name) as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            if i == 0:
                i += 1
                continue
            list = line.split('\n')[0].split(' ')
            value = list[len(list) - 1]
            res.append(float(value))
    res2 = []
    f_name = "test2.txt"
    with open(f_name) as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            if i == 0:
                i += 1
                continue
            list = line.split('\n')[0].split(' ')
            value = list[len(list) - 1]
            res2.append(float(value))
    res3 = []
    f_name = "test3.txt"
    with open(f_name) as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            if i == 0:
                i += 1
                continue
            list = line.split('\n')[0].split(' ')
            value = list[len(list) - 1]
            res3.append(float(value))
    x = []
    for i in range(1,101):
        x.append(i)

    x_axis_data = x
    y_axis_data = res

    plt.plot(x_axis_data, y_axis_data ,color='#4169E1', alpha=0.8, linewidth=1.2,label = 'client1')
    y_axis_data = res2
    plt.plot(x_axis_data, y_axis_data,  color='black', alpha=0.8, linewidth=1.2,label = 'client2')
    y_axis_data = res3
    plt.plot(x_axis_data, y_axis_data, color='green', alpha=0.8, linewidth=1.2, label='client3')
    plt.title('the latency graph with 3 clients with loss in scenario3')
    plt.legend(loc="upper right")
    plt.xlabel('iteration times')
    plt.ylabel('latency')
    plt.show()
