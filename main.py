from . import sv, log, Port, SAMPLE, BOTNAME
import json
import os
from pathlib import Path
import subprocess
import sys

from hoshino.typing import CQEvent
from hoshino import priv
from nonebot import get_bot
from nonebot import on_websocket_connect
import runpy


@on_websocket_connect
async def start_up(ev: CQEvent):
    if not SAMPLE.exists():
        data = {}
        with open(SAMPLE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    with open(SAMPLE, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    bot = get_bot()
    
    try:
        with open(SAMPLE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):  # 确保data是字典
                data = {}
                with open(SAMPLE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    try:
        if data["reboot"] == "True":
            group_id = data["group_id"]
            await bot.send_group_msg(group_id=group_id, message=(f"[{BOTNAME} 启动成功]"))
            data["reboot"] = "False"
            with open(SAMPLE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log.error(f"发送失败：{e}")
        
@sv.on_prefix('/sudo')
async def sudo(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        try:
            await bot.delete_msg(message_id=ev.message_id)
        except Exception as e:
            pass
        
        await bot.send(ev, "你没资格啊你没资格")
        return
    args = str(ev.message).split()
    
    try:
        with open(SAMPLE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):  # 确保data是字典
                data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
        
    if args[0] == "reboot":
        msg_id = await bot.send(ev, f"[{BOTNAME} 重启中...]")
        data["message_id"] = msg_id.get('message_id', None)
        data["reboot"] = "True"
        data["group_id"] = int(ev.group_id)
        
        with open(SAMPLE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        reboot_script = Path(__file__).parent / "libraries" / "reboot_helper.py"
        python = sys.executable
        Hoshino_ROOT = Path(__file__).parent.parent.parent.parent
        run_path = str(Hoshino_ROOT / "run.py")

        if not reboot_script.exists():
            await bot.send(ev, "重启脚本未找到，重启失败")
            log.info("重启脚本未找到:", reboot_script)
            return

        reboot_command = [
            python,
            str(reboot_script),
            run_path,
            str(Port)
        ]

        try:
            # 使用新窗口运行重启脚本
            subprocess.Popen(reboot_command, creationflags=subprocess.CREATE_NEW_CONSOLE)
            log.info(f"重启脚本已启动: {' '.join(reboot_command)}")
            os._exit(0)
        except Exception as e:
            log.info(f"启动重启脚本失败: {e}")
            await bot.send(ev, f"{BOTNAME} 重启失败")