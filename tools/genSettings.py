#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json

if __name__ == "__main__":
    obj = json.load(open(sys.argv[1], mode="r"))
    head = """/*
 * Copyright (C) 2019-2020 Ashar Khan <ashar786khan@gmail.com>
 *
 * This file is part of CP Editor.
 *
 * CP Editor is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * I will not be responsible if CP Editor behaves in unexpected way and
 * causes your ratings to go down and or lose any important contest.
 *
 * Believe Software is "Software" and it isn't immune to bugs.
 *
 */

/*
 * This file is auto generated by tools/genSettings.py
 */

"""
    setting_helper = open("generated/SettingsHelper.hpp", mode="w")
    setting_helper.write(head)
    setting_helper.write("""#ifndef SETTINGSHELPER_HPP
#define SETTINGSHELPER_HPP

#include "Settings/SettingsManager.hpp"
#include <QFont>
#include <QRect>

namespace SettingsHelper
{
""")
    for t in obj:
        name = t["name"]
        key = name.replace(" ", "").replace("/", "").replace("+", "p")
        typename = t["type"]
        setting_helper.write(f"    inline void set{key}({typename} value) {{ SettingsManager::set({json.dumps(name)}, value); }}\n")
        if typename == "bool":
            setting_helper.write(f"    inline bool is{key}() {{ return SettingsManager::get({json.dumps(name)}).toBool(); }}\n")
        else:
            setting_helper.write(f"    inline {typename} get{key}() {{ return SettingsManager::get({json.dumps(name)}).value<{typename}>(); }}\n")
    setting_helper.write("""}

#endif // SETTINGSHELPER_HPP""")
    setting_helper.close()
    setting_info = open("generated/SettingsInfo.hpp", mode="w")
    setting_info.write(head)
    setting_info.write("""#ifndef SETTINGSINFO_HPP
#define SETTINGSINFO_HPP

#include <QString>
#include <QFont>
#include <QRect>
#include <QByteArray>
#include <QVariant>

struct SettingInfo
{
    QString name, desc, type, ui, tip;
    QStringList old;
    QVariant def;
    QVariant param;

    QString key() const
    {
        return name.toLower().replace('+', 'p').replace(' ', '_');
    }
};

const SettingInfo settingInfo[] =
{
""")
    for t in obj:
        name = t["name"]
        typename = t["type"]
        if "desc" in t:
            desc = t["desc"]
        else:
            desc = name.replace('/', ' ')
        if "ui" in t:
            ui = t["ui"]
        else:
            ui = ""
        if "tip" in t:
            tip = t["tip"]
        else:
            tip = ""
        setting_info.write(f"    {{{json.dumps(name)}, {json.dumps(desc)}, \"{typename}\", \"{ui}\", {json.dumps(tip)}, {{")
        if "old" in t:
            olds = ""
            for s in t["old"]:
                olds = olds + '"' + s + '", '
            setting_info.write(olds)
        setting_info.write("}, ")
        if "default" in t:
            if typename == "QString":
                setting_info.write(json.dumps(t["default"]))
            else:
                if isinstance(t["default"], bool):
                    setting_info.write(str(t["default"]).lower())
                else:
                    setting_info.write(str(t["default"]))
        else:
            defs = {
                'QString':'""',
                'int': '0',
                'bool': 'false',
                'QRect': 'QRect()',
                'QByteArray': 'QByteArray()'
            }
            setting_info.write(defs[typename])
        if "param" in t:
            setting_info.write(f', {t["param"]}')
        setting_info.write("},\n")
    setting_info.write("""};

inline SettingInfo findSetting(const QString &name)
{
    for (const SettingInfo &si: settingInfo)
        if (si.name == name)
            return si;
    return SettingInfo();
}

#endif // SETTINGSINFO_HPP""")
    setting_info.close()