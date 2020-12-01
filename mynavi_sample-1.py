import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
# 正規表現
import re
# ログ
import logging
# ログの設定
logging.basicConfig(filename="ProgramLog.log",level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("プログラム開始")


# ２次元配列を１次元配列に修正
def flattening(two,c,w):
    if two[c]:
        two[c] = two[c][0].replace(w, '')
        two[c] = two[c].replace("\n", '')
    else:
        two[c] = "取得できませんでした"
# 各リストから"shift_jis"に対応していない文字の消去
def codec(job,n):
    job[n] = job[n].replace("\uff5e","").replace("\u2014","")


# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        print("ポップアップがありません")
        time.sleep(5)

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()



    for page in range(2,4):
        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

        #　課題２．
        #　name_listから会社の条件を取り出す
        tableCondition_list = driver.find_elements_by_class_name("tableCondition")
        #tableCondition_head_list = driver.find_elements_by_class_name("tableCondition__head")
        #tableCondition_body_list = driver.find_elements_by_class_name("tableCondition__body")

        # 会社名を抽出
        company_name = re.compile(r".*\|")
        #job description = re.compile()

        company_name_list = []
        count = 0

        job1 = []
        job2 = []
        job3 = []
        job4 = []

        job_c = re.compile(r"仕事内容 .+\n")
        job_t = re.compile(r"対象となる方 .+\n")
        job_p = re.compile(r"勤務地 .+\n")
        job_s = re.compile(r"給与 .+\n")

        for (name,tableCondition) in zip(name_list,tableCondition_list):
            # name.textから会社名だけ抽出
            company_name_list.append(company_name.findall(name.text))
            # ２次元配列を１次元配列に修正 , company_name_listから" |"を消す
            company_name_list[count] = company_name_list[count][0].replace(' |', '')

            # tableCondition.textから仕事内容だけ抽出
            job1.append(job_c.findall(tableCondition.text))
            # ２次元配列を１次元配列に修正 , jobから"仕事内容"と"\n"を消す
            flattening(job1,count,"仕事内容 ")
            #tableCondition.textから対象となる方だけ抽出
            job2.append(job_t.findall(tableCondition.text))
            # ２次元配列を１次元配列に修正 , jobから"対象となる方"と"\n"を消す
            flattening(job2,count,"対象となる方 ")
            # tableCondition.textから勤務地だけ抽出
            job3.append(job_p.findall(tableCondition.text))
            # ２次元配列を１次元配列に修正 , jobから"勤務地"と"\n"を消す
            flattening(job3,count,"勤務地 ")
            # tableCondition.textから給与だけ抽出
            job4.append(job_s.findall(tableCondition.text))
            # ２次元配列を１次元配列に修正 , jobから"給与"と"\n"を消す
            flattening(job4,count,"給与 ")

            # ログ出力
            logging.debug("count = {},naem = {}, tableCondition = {}".format(count,name.text,tableCondition.text))
            logging.debug("company_name_list[count] = {}".format(company_name_list[count]))
            logging.debug("job1[count] = {}".format(job1[count]))
            logging.debug("job2[count] = {}".format(job2[count]))
            logging.debug("job3[count] = {}".format(job3[count]))
            logging.debug("job4[count] = {}".format(job4[count]))
            count += 1



        print("{}ページ目\n\n".format(page-1))
        # 会社名を表示
        print("会社名\n",company_name_list,"\n\n")
        # 仕事内容を表示
        print("仕事内容\n",job1,"\n\n")
        # 対象となる方を表示
        print("対象となる方\n",job2,"\n\n")
        # 勤務地を表示
        print("勤務地\n",job3,"\n\n")
        # 給与を表示
        print("給与\n",job4,"\n\n")
        # 各リストから"shift_jis"に対応していない文字の消去
        for n in range(0,len(company_name_list)):
            codec(company_name_list,n)
            codec(job1,n)
            codec(job2,n)
            codec(job3,n)
            codec(job4,n)
        df1 = pd.DataFrame([company_name_list])
        df2 = pd.DataFrame([job1])
        df3 = pd.DataFrame([job2])
        df4 = pd.DataFrame([job3])
        df5 = pd.DataFrame([job4])
        # CSV ファイル (employee.csv) として出力
        df1.to_csv("employee.csv", mode='a', header=False, encoding="shift_jis")
        df2.to_csv('employee.csv', mode='a', header=False, encoding="shift_jis")
        df3.to_csv('employee.csv', mode='a', header=False, encoding="shift_jis")
        df4.to_csv('employee.csv', mode='a', header=False, encoding="shift_jis")
        df5.to_csv('employee.csv', mode='a', header=False, encoding="shift_jis")

        # コンソールから検索
        search = input(str("このページで何か検索しますか？（yes or no）:"))
        if search == "yes":
            for nmber in range(0,len(company_name_list)):
                print("{}:{}".format(nmber,company_name_list[nmber]))


            search_n = input("\nどの会社の情報を検索しますか？（番号を入力してください）:")
            print("会社名:{}".format(company_name_list[int(search_n)]))
            print("仕事内容:{}".format(job1[int(search_n)]))
            print("対象となる方:{}".format(job2[int(search_n)]))
            print("勤務地:{}".format(job3[int(search_n)]))
            print("給与:{}".format(job4[int(search_n)]))
            
        # 各リストの初期化
        company_name_list.clear()
        job1.clear()
        job2.clear()
        job3.clear()
        job4.clear()

        # 次のページ目をクリック
        driver.find_element_by_link_text(str(page)).click()
        time.sleep(5)








# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
