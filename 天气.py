import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

# 基本参数配置
API_URL = 'http://apis.juhe.cn/simpleWeather/query'  # 接口请求URL
API_KEY = 'dacc648ee1120004c8dee9d2476b43d3'  # 聚合数据申请的key

def get_weather(city_name):
    """查询指定城市的天气信息并返回格式化字符串"""
    request_params = {
        'key': API_KEY,
        'city': city_name,
    }

    try:
        response = requests.get(API_URL, params=request_params, timeout=5)
        response.raise_for_status()  # 如果请求失败，则抛出HTTPError异常
        result = response.json()

        if result and result['error_code'] == 0:
            weather_info = result['result']
            realtime = weather_info['realtime']
            
            return (
                f"查询城市: {weather_info['city']}\n"
                f"------实时天气------\n"
                f"天气: {realtime['info']}\n"
                f"温度: {realtime['temperature']}℃\n"
                f"湿度: {realtime['humidity']}%\n"
                f"风向: {realtime['direct']}\n"
                f"风力: {realtime['power']}\n"
                f"空气质量指数: {realtime['aqi']}\n"
                f"---------------------\n"
            )
        else:
            return f"查询失败: {result.get('reason', '未知错误')}"

    except requests.exceptions.RequestException as e:
        return f"网络请求异常: {e}"
    except KeyError:
        return "解析返回数据失败，请检查API返回格式是否变更"
    except Exception as e:
        return f"发生未知错误: {e}"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("天气查询系统")
        self.root.geometry("400x350")

        # 城市输入框
        self.city_label = tk.Label(root, text="请输入城市名称:")
        self.city_label.pack(pady=5)
        self.city_entry = tk.Entry(root, width=30)
        self.city_entry.pack(pady=5)

        # 查询按钮
        self.search_button = tk.Button(root, text="查询天气", command=self.search_weather)
        self.search_button.pack(pady=10)

        # 结果显示框
        self.result_text = scrolledtext.ScrolledText(root, width=45, height=15, wrap=tk.WORD)
        self.result_text.pack(pady=10, padx=10)

    def search_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("输入错误", "城市名称不能为空！")
            return
        
        self.result_text.delete(1.0, tk.END) # 清空上次结果
        self.result_text.insert(tk.INSERT, "正在查询，请稍候...")
        self.root.update_idletasks()

        weather_result = get_weather(city)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.INSERT, weather_result)

if __name__ == '__main__':
    main_window = tk.Tk()
    app = WeatherApp(main_window)
    main_window.mainloop()
    print('请求异常')