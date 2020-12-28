import tkinter as tk
import time
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import cv2
from PIL import Image, ImageTk
from Commands import UnitCommand
import requests
import json
import os
import datetime


# GUI of switch controller simulator
class GetFromHomeGUI:
    def __init__(self, root):
        self.poke_window = tk.Toplevel(root)
        self.poke_window.title('技採用率')
        # self.poke_window.geometry("%dx%d%+d%+d" % (600, 300, 250, 125))
        # self.poke_window.resizable(0, 0)
        # joycon_L_frame = tk.Frame(self.window, width=300, height=300, relief='flat')
        # joycon_L_frame.grid(row=0, column=0)

        self.rank_match_result_dic = self.get_rank_match_result()
        self.poke_data = None
        self.season_list = list(self.rank_match_result_dic['list'].keys())[::-1]
        self.rule_list = ["シングル", "ダブル"]
        self.columns = ('図鑑番号', '種類', 'フォルム(番号)', 'タイプ1', 'タイプ2')
        self.columns_d = ('技', '採用率',
                          '特性', '採用率　',
                          '性格', '採用率　　　',
                          '持ち物', '採用率　　　　',
                          '一緒に採用されるポケモン',
                          'このポケモンを倒した技', '割合',
                          'このポケモンを倒したポケモン',
                          'このポケモンが相手を倒した技', '割合 ',
                          'このポケモンが倒したポケモン')

        self.treeview = ttk.Treeview(self.poke_window, columns=self.columns, show='headings', selectmode='browse')
        self.treeview_detail = ttk.Treeview(self.poke_window, columns=self.columns_d, show='headings',
                                            selectmode='browse')
        self.vsb = ttk.Scrollbar(self.poke_window, orient="vertical", command=self.treeview.yview)
        self.hsb = ttk.Scrollbar(self.poke_window, orient="horizontal", command=self.treeview.xview)
        self.vsb_d = ttk.Scrollbar(self.poke_window, orient="vertical", command=self.treeview_detail.yview)
        self.hsb_d = ttk.Scrollbar(self.poke_window, orient="horizontal", command=self.treeview_detail.xview)
        self.season_l = ttk.Label(self.poke_window, text="ランクシーズン")
        self.isSingle_l = ttk.Label(self.poke_window, text="バトルの種類")
        self.season = tk.StringVar(value=self.season_list[-1])
        self.isSingle = tk.StringVar(value=self.rule_list[0])
        self.getRankPokeData_Button = ttk.Button(self.poke_window, text="取得", command=self.getRankPokeData)
        self.getPokeDetail_Button = ttk.Button(self.poke_window, text="詳細取得", command=self.getPokeDetail)

        self.season_cb = ttk.Combobox(self.poke_window, textvariable=self.season, values=self.season_list, width=30,
                                      state="readonly")
        self.season_cb.current(self.season_cb['values'].index(self.season.get()))
        self.isSingle_cb = ttk.Combobox(self.poke_window, textvariable=self.isSingle, values=self.rule_list, width=80,
                                        state="readonly")
        self.isSingle_cb.current(self.isSingle_cb['values'].index(self.isSingle.get()))

        self.treeview.configure(yscrollcommand=self.vsb.set)
        self.treeview.configure(xscrollcommand=self.hsb.set)
        self.treeview_detail.configure(yscrollcommand=self.vsb.set)
        self.treeview_detail.configure(xscrollcommand=self.hsb.set)

        for col in self.columns:
            self.treeview.column(col, minwidth=0, width=90, stretch=tk.NO)
            self.treeview.heading(col, text=col,
                                  command=lambda _col=col: self.treeview_sort_column(self.treeview, _col, False))
        _ = 0
        for col in self.columns_d:
            if _ in [0, 4]:
                self.treeview_detail.column(col, minwidth=0, width=100, stretch=tk.NO)
            elif _ in [1, 2, 3, 5, 6, 7, 10, 13]:
                self.treeview_detail.column(col, minwidth=0, width=80, stretch=tk.NO)
            else:
                self.treeview_detail.column(col, minwidth=0, width=150, stretch=tk.NO)

            self.treeview_detail.heading(col, text=col,
                                         command=lambda _col=col: self.treeview_sort_column(self.treeview_detail,
                                                                                            _col,
                                                                                            False))
            _ += 1

        self.season_l.grid(row=0, column=0, sticky='news')
        self.season_cb.grid(row=0, column=1, sticky='news')
        self.isSingle_l.grid(row=0, column=2, sticky='news')
        self.isSingle_cb.grid(row=0, column=3, sticky='news')
        self.getRankPokeData_Button.grid(row=0, column=4, columnspan=2, sticky='news')
        self.getPokeDetail_Button.grid(row=1, column=5, sticky='news')
        self.treeview.grid(row=1, column=0, columnspan=4, sticky='news')
        self.treeview_detail.grid(row=3, column=0, columnspan=4, sticky='news')
        self.vsb.grid(row=1, column=4, sticky='nsw')
        self.hsb.grid(row=2, column=0, columnspan=4, sticky='ew')
        self.vsb_d.grid(row=3, column=4, sticky='nsw')
        self.hsb_d.grid(row=4, column=0, columnspan=4, sticky='ew')

        self.vsb.configure(command=self.treeview.yview)
        self.hsb.configure(command=self.treeview.xview)
        self.vsb_d.configure(command=self.treeview_detail.yview)
        self.hsb_d.configure(command=self.treeview_detail.xview)

        self.setPokemons()

    def getPokeDetail(self):
        self.delDetail()
        selected_items = self.treeview.selection()
        if not selected_items:
            return None
        values = self.treeview.item(selected_items[0], 'values')
        self.makePokeDetailList(values)

    def delDetail(self):
        x = self.treeview_detail.get_children()
        for item in x:
            self.treeview_detail.delete(item)

    def makePokeDetailList(self, values):
        waza = [["", ""] for _ in range(10)]
        tokusei = [["", ""] for _ in range(10)]
        seikaku = [["", ""] for _ in range(10)]
        motimono = [["", ""] for _ in range(10)]
        withPokemon = [["", ""] for _ in range(10)]
        beatedWaza = [["", ""] for _ in range(10)]
        beatedPoke = [["", ""] for _ in range(10)]
        beatWaza = [["", ""] for _ in range(10)]
        beatPokemon = [["", ""] for _ in range(10)]
        for i in range(10):
            try:  # 凄く強引な実装なので修正したい…
                try:
                    waza[i] = [self.poke_data[values[0]][values[2]]["temoti"]["waza"][i]["id"],
                               self.poke_data[values[0]][values[2]]["temoti"]["waza"][i]["val"] + "%"]
                except:
                    pass
                try:
                    tokusei[i] = [self.poke_data[values[0]][values[2]]["temoti"]["tokusei"][i]["id"],
                                  self.poke_data[values[0]][values[2]]["temoti"]["tokusei"][i]["val"] + "%"]
                except:
                    pass
                try:
                    seikaku[i] = [self.poke_data[values[0]][values[2]]["temoti"]["seikaku"][i]["id"],
                                  self.poke_data[values[0]][values[2]]["temoti"]["seikaku"][i]["val"] + "%"]
                except:
                    pass
                try:
                    motimono[i] = [self.poke_data[values[0]][values[2]]["temoti"]["motimono"][i]["id"],
                                   self.poke_data[values[0]][values[2]]["temoti"]["motimono"][i]["val"] + "%"]
                except:
                    pass
                try:
                    withPokemon[i] = [self.poke_data[values[0]][values[2]]["temoti"]["pokemon"][i]["id"],
                                      self.poke_data[values[0]][values[2]]["temoti"]["pokemon"][i]["form"]]
                except:
                    pass
                try:
                    beatedWaza[i] = [self.poke_data[values[0]][values[2]]["lose"]["waza"][i]["id"],
                                     self.poke_data[values[0]][values[2]]["lose"]["waza"][i]["val"] + "%"]
                except:
                    pass
                try:
                    beatedPoke[i] = [self.poke_data[values[0]][values[2]]["lose"]["pokemon"][i]["id"],
                                     self.poke_data[values[0]][values[2]]["lose"]["pokemon"][i]["form"]]
                except:
                    pass
                try:
                    beatWaza[i] = [self.poke_data[values[0]][values[2]]["win"]["waza"][i]["id"],
                                   self.poke_data[values[0]][values[2]]["win"]["waza"][i]["val"] + "%"]
                except:
                    pass
                try:
                    beatPokemon[i] = [self.poke_data[values[0]][values[2]]["win"]["pokemon"][i]["id"],
                                      self.poke_data[values[0]][values[2]]["win"]["pokemon"][i]["form"]]
                except:
                    pass
            except:
                pass
        for i in range(10):
            self.treeview_detail.insert("", "end", values=(
                self.ja_pokes["waza"][waza[i][0]] if waza[i][0] != "" else "", waza[i][1],
                self.ja_pokes["tokusei"][tokusei[i][0]] if tokusei[i][0] != "" else "", tokusei[i][1],
                self.ja_pokes["seikaku"][seikaku[i][0]] if seikaku[i][0] != "" else "", seikaku[i][1],
                self.ja_pokes["item"][motimono[i][0]] if motimono[i][0] != "" else "", motimono[i][1],
                self.ja_pokes["poke"][withPokemon[i][0] - 1] if withPokemon[i][0] != "" else "",
                self.ja_pokes["waza"][beatedWaza[i][0]] if beatedWaza[i][0] != "" else "", beatedWaza[i][1],
                self.ja_pokes["poke"][beatedPoke[i][0] - 1] if beatedPoke[i][0] != "" else "",
                self.ja_pokes["waza"][beatWaza[i][0]] if beatWaza[i][0] != "" else "", beatWaza[i][1],
                self.ja_pokes["poke"][beatPokemon[i][0] - 1] if beatPokemon[i][0] != "" else ""
            ))

    def getRankPokeData(self):
        if self.isSingle.get() == "シングル":
            isSingle = 1
        else:
            isSingle = 0
        print(isSingle,list(self.rank_match_result_dic['list'][self.season.get()].keys())[1 - isSingle])
        poke_w = self.get_rank_poke_data(
            list(self.rank_match_result_dic['list'][self.season.get()].keys())[1 - isSingle],
            self.rank_match_result_dic['list'][self.season.get()][str(10001 + 10 * int(self.season.get()) + isSingle)][
                'rst'],
            self.rank_match_result_dic['list'][self.season.get()][str(10001 + 10 * int(self.season.get()) + isSingle)][
                'ts2']
        )
        self.poke_data = poke_w

    def setPokemons(self):
        f = open('db/pokedex.json', 'r', encoding="utf-8")
        json_data = json.load(f)
        self.ja_pokes = json_data['dex']['ja']
        poke_list = self.ja_pokes['poke']
        poke_types = self.ja_pokes['pokeType']
        poke_type = json_data['pokemonType']
        for dex_num in poke_type.keys():
            for poke_form in poke_type[dex_num].keys():
                poke_type1, poke_type2 = self.pokemonType(poke_types, *poke_type[dex_num][poke_form])
                self.treeview.insert("", "end",
                                     values=(
                                         int(dex_num), poke_list[int(dex_num) - 1], poke_form, poke_type1, poke_type2))
            # 下はもっと泥臭い実装。わかりやすいけどあまりに面倒だったので諦めました…
            # if dex_num == "876":
            #     self.treeview.insert("", "end", values=(dex_num, "イエッサン♂"))
            #     self.treeview.insert("", "end", values=(dex_num, "イエッサン♀"))
            # elif dex_num == "479":
            #     self.treeview.insert("", "end", values=(dex_num, "ロトム（通常）"))
            #     self.treeview.insert("", "end", values=(dex_num, "ロトム（火）"))
            #     self.treeview.insert("", "end", values=(dex_num, "ロトム（水）"))
            #     self.treeview.insert("", "end", values=(dex_num, "ロトム（氷）"))
            #     self.treeview.insert("", "end", values=(dex_num, "ロトム（飛行）"))
            #     self.treeview.insert("", "end", values=(dex_num, "ロトム（草）"))
            # elif dex_num == "898":
            #     self.treeview.insert("", "end", values=(dex_num, "バドレックス"))
            #     self.treeview.insert("", "end", values=(dex_num, "バドレックス（白馬）"))
            #     self.treeview.insert("", "end", values=(dex_num, "バドレックス（黒馬）"))
            # else:
            #     self.treeview.insert("", "end", values=(dex_num, poke_name))

    def pokemonType(self, poke_types, t1, t2=None):
        if t2 == None:
            return poke_types[int(t1)], ""
        else:
            return poke_types[int(t1)], poke_types[int(t2)]

    def treeview_sort_column(self, tv, col, reverse):
        try:
            l = [
                (int(tv.set(k, col)), k) for k in tv.get_children("")
            ]
        except Exception:
            l = [(tv.set(k, col), k) for k in tv.get_children("")]

        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(tv, _col, not reverse))

    def get_rank_match_result(self):
        path = 'db/rank_match.json'
        headers_rank_match_list = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'countrycode': '304',
            'authorization': 'Bearer',
            'langcode': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
            'content-type': 'application/json',
        }
        data = '{"soft":"Sw"}'
        hours, minutes, seconds = 0, 0, 0
        if os.path.exists(path):
            LastFileGetTime = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
            nowtime = datetime.datetime.now()
            delta_time = nowtime - LastFileGetTime
            days, seconds = delta_time.days, delta_time.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            print("最後にランクマッチデータをDLしたのは{0}時間{1}分{2}秒前".format(hours, minutes, seconds))

        # ファイルが存在しないまたは最後のDLから45分経っているときは新しくダウンロードする
        if not os.path.exists(path) or minutes >= 45:
            try:
                print("ランクマッチのデータをダウンロード中…", end="")
                response = requests.post('https://api.battle.pokemon-home.com/cbd/competition/rankmatch/list',
                                         headers=headers_rank_match_list,
                                         data=data)
                print("完了。保存中…", end="")
                data_ = response.json()
                with open(path, 'w') as outfile:
                    json.dump(data_, outfile, indent=4)
                print("完了。")
            except:
                data_ = None
                print("Error: レスポンスが得られませんでした。")
                if os.path.exists(path):
                    print("過去にDLしたデータを利用してデータ取得を試みます。")
                    with open(path, "r") as json_file:
                        data_ = json.load(json_file, encoding="utf-8")
        else:
            print("過去にDLしたランクマッチのデータを利用します。")
            with open(path, "r") as json_file:
                data_ = json.load(json_file, encoding="utf-8")
        return data_

    def get_rank_poke_data(self, isSingle, rst, ts2):
        l = "Single" if self.isSingle.get() == "シングル" else "Double"
        path = "db/pokedata_Season" + self.season.get() + "_" + l + "Battle" + ".json"
        headers_rank_poke_data = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
            'accept': 'application/json',
        }
        poke_dic = {}

        hours, minutes, seconds = 0, 0, 0
        if os.path.exists(path):
            LastFileGetTime = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
            nowtime = datetime.datetime.now()
            delta_time = nowtime - LastFileGetTime
            days, seconds = delta_time.days, delta_time.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            print("最後にシーズン{0}/{1}バトルのデータをDLしたのは{2}時間{3}分{4}秒前".format(
                self.season.get(), self.isSingle.get(), hours, minutes, seconds))
        if not os.path.exists(path) or hours >= 24 or (rst == 2 and not os.path.exists(path)):
            try:
                print("シーズン{}/{}バトルのポケモンデータをダウンロード中…".format(
                    self.season.get(), self.isSingle.get()), end="")

                for i in range(1, 6):
                    response = requests.get(
                        'https://resource.pokemon-home.com/battledata/ranking/{0}/{1}/{2}/pdetail-{3}'.format(
                            isSingle,
                            rst,
                            ts2, i),
                        headers=headers_rank_poke_data
                    )
                    _ = response.json()
                    print("{}/5 完了".format(i))
                    poke_dic.update(_)
                print("保存中…", end="")
                with open(path, 'w') as outfile:
                    json.dump(poke_dic, outfile, indent=4)
                print("完了。")
            except:
                print("Error: レスポンスが得られませんでした。")
                if os.path.exists(path):
                    print("過去にDLしたデータを利用します。")
                    with open(path, "r") as json_file:
                        poke_dic = json.load(json_file, encoding="utf-8")
        else:
            print("過去にDLしたデータを利用します。")
            with open(path, "r") as json_file:
                poke_dic = json.load(json_file, encoding="utf-8")

        return poke_dic

    def bind(self, event, func):
        self.poke_window.bind(event, func)

    def protocol(self, event, func):
        self.poke_window.protocol(event, func)

    def focus_force(self):
        self.poke_window.focus_force()

    def destroy(self):
        self.poke_window.destroy()