import datetime
import threading
import time
mark_time=" 20:30:00.100000"
# 修改：上面的marktime改成你需要的自启动时间即可
# (空格别删了)请按照以上格式修改时间哦  乱修改会报错
 
# 运行函数
def func(n=5):
    # 在这里加你的函数即可
    pass   #等待窗口弹出
    
# preFun预处理函数  对第一次启动进行今日或次日时间判断  然后方便进行正确的自启动
def preFun(marktime):
    '''
    返回下次执行与现在的秒数,如果时间已过则显示“明日XXX执行代码”
    '''
    # 获取现在时间
    now_time = datetime.datetime.now()
    marktimes = datetime.datetime.strptime(str(now_time.date()) + marktime, "%Y-%m-%d %H:%M:%S.%f")
    # marktimes是datetime化的时间数据类型
    # 2020-03-13 17:35:26.772379  marktimes是如左类似结构
    # 今日时间是否预期
    if (now_time <= marktimes):
        next_time = marktimes
        print("今日" + marktime + '执行代码')
    else:
        # 明日启动
        next_time = now_time + datetime.timedelta(days=+1)
        print("明日" + marktime + '执行代码')
 
    # 这下面可以优化
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
 
    next_time = datetime.datetime.strptime(str(next_year) +
                                           "-" + str(next_month) +
                                           "-" + str(next_day) + marktime,
                                           "%Y-%m-%d %H:%M:%S.%f")
    # next_time将得到的下次时间更新成秒数表示的时间
    # 科普一下 就是那种time.time()函数得到的秒  这样的时间方便计算  不然要疯狂的进制转化……
    # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）。
    # 获取距离下次marktime时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    return timer_start_time
def main():
    timer_start_time=preFun(mark_time)
    # 把与处理得时间放进去  然后线程在start（）后
    # 会在规定秒数后启动你的func里的代码
    timer = threading.Timer(timer_start_time, func, args=[1])#最后面的参数表示func执行的次数
    # 运行线程
    timer.start()
    print('冷启动后启动func的时间',timer_start_time)
    pass
if __name__ == '__main__':
    main()

 