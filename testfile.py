import discord
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import random
import os
from discord.utils import get

client = commands.Bot(command_prefix=">>", intents=discord.Intents.all())

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

url = 'https://docs.google.com/spreadsheets/d/1WI7W0KjLaebqQUuLpf7BqhPYEKnLa2ppNLEiXasOce4/edit#gid=0'

current_time = lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=9)


def is_moderator(member):
    return "운영진" in map(lambda x: x.name, member.roles)

def is_dcstaff(member):
    return "스텝-DC" in map(lambda x: x.name, member.roles)

@client.event
async def on_ready():
    global Harang
    await client.wait_until_ready()
    game = discord.Game("신입클랜원 환영")
    print("login: Harang Main")
    print(client.user.name)
    print(client.user.id)
    print("---------------")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_member_join(member):
    role = get(member.guild.roles, name="신입클랜원")

    embed = discord.Embed(title="하랑에 오신 것을 환영합니다", description="하랑에 대해 간단히 설명해드릴게요!", color=12745742)
    embed.add_field(name="필독 링크", value="네이버 카페 링크 : https://cafe.naver.com/owgreen \n "
                                        "필독 공지 : https://cafe.naver.com/owgreen/10862 \n "
                                        "하랑봇 사용법 : https://cafe.naver.com/owgreen/9547", inline=False)
    embed.add_field(name="Q0. 운영진 및 스텝 친추를 꼭! 해야한다던데.. 누가 운영진이고 스텝이죠?",
                    value="디스코드 대화공간 채널에서 >>운영진  이라고 쳐보시면 운영진 및 스텝 명단을 볼 수 있습니다. 꼭 친추 하셔야해요!", inline=False)
    embed.add_field(name="Q1. 별명은 어떻게 바꾸나요?",
                    value="디스코드 기준 왼쪽에 하랑서버에서 우클릭 > 별명 변경하기 > (나이/포지션)닉네임#배틀태그", inline=False)
    embed.add_field(name="Q2. 별명 변경시 저는 Flex인데 Flex로 별명 변경 가능한가요?",
                    value="아니요. 하랑에 지원하실 때 적은 대표 포지션으로만 변경 가능합니다. "
                          "포지션을 추가하고 싶으시면 정식 클랜원이 되신 이후 테스트내전을 통해 포지션을 획득할 수 있습니다.",
                    inline=False)
    embed.add_field(name="Q3. 큐는 어떻게 들어가면 되나요?",
                    value="각 큐의 남는 포지션을 보고 들어가시면 됩니다. 잘모르겠다면 직접 음성방에 들어가서 물어보시거나 "
                          "디코의 #대화공간에서 9번방 탱커자리 있나요? 이런식으로 물어보시면 친절하게 답해주실거에요",
                    inline=False)
    embed.add_field(name="Q4. 솔로로 돌리고 싶습니다 그럼 디코는 사용하지 않아도 되나요?",
                    value="솔큐로 플레이 하실 때에는 디스코드의 솔큐방에 들어가신 후 플레이 부탁드립니다. "
                          "또, 지인과 플레이 하거나 타 디코를 사용할 때에는 디스코드 #대화공간에 언급해 주신 후 플레이 부탁드립니다.",
                    inline=False)
    embed.add_field(name="Q5. 연습방이란 무엇인가요?",
                    value="본인 포지션이 아닌 타포지션을 연습하기 위한 방입니다. "
                          "연습방에서는 포지션의 제한 없이 모든 포지션을 플레이 하실 수 있습니다.",
                    inline=False)
    embed.add_field(name="Q6. 수다방에서 나갔는데 다시 들어가려면 링크가 필요해요!",
                    value="하랑봇을 사용해서 보실 수 있습니다 디스코드 #대화공간에서 >>수다방 이라고 타이핑하시면 "
                          "오픈카톡방 링크를 확인하실 수 있습니다. 하랑봇는 여러 기능이 많으니 위에 첨부한 하랑봇 가이드 링크를 참고해주세요.",
                    inline=False)
    await member.send(embed=embed)
    await member.add_roles(role)


async def get_spreadsheet(ws_name):
    creds = ServiceAccountCredentials.from_json_keyfile_name("HarangTest-130d0649c09f.json", scope)
    auth = gspread.authorize(creds)

    if creds.access_token_expired:
        auth.login()

    try:
        worksheet = auth.open_by_url(url).worksheet(ws_name)
    except gspread.exceptions.APIError:
        print("API Error")
        return
    return worksheet


async def has_role(member, role):
    return role in map(lambda x: x.name, member.roles)


async def get_member_by_battletag(battletag):
    global harang
    harang = client.get_guild(406688488671543297)

    for member in harang.members:
        try:
            if member.nick.endswith(battletag):
                return member
        except:
            continue


async def get_opener(self):
    ws = await get_spreadsheet('current_scream')
    return ws.cell(1, 1).value


async def is_spreadsheet_empty(sheetname):
    ws = await get_spreadsheet(sheetname)
    if ws.cell(1, 1).value is "":
        return True
    else:
        return False


@client.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel

    print('{} / {}: {}'.format(channel, author, content))

    if message.content.startswith(">>"):
        content = message.content
        content = content.split(">>")
        content = content[1]

        if content == '':
            return

        if content == "팀편성":
            await message.channel.send("@here 팀편성 해주세요!\n" + "https://tenor.com/view/thinking-think-tap-tapping-spongebob-gif-5837190")
            return

        if content.startswith("스크림개최"):
            opener = author.mention
            time = content.split(" ")[1]
            limit = content.split(" ")[2]
            desc = content[15:]

            # 개최될 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is False:
                await message.channel.send("이미 개최될 스크림이 있습니다")
                return

            # 개최자 자동 1번 등록
            ws = await get_spreadsheet('current_scream_list')
            ws.resize(rows=1, cols=1)
            ws.append_row([author.mention])

            ws = await get_spreadsheet('current_scream')
            ws.resize(rows=4, cols=1)

            ws.append_row([opener])
            ws.append_row([time])
            ws.append_row([limit])
            ws.append_row([desc])

            await message.channel.send("@everyone \n 오늘 {} 스크림이 열립니다. \n 주최자 : {} \n 제한인원 : {}명".format(time, author.mention, limit))
            return

        if content == "스크림신청":
            # 예정된 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is True:
                await message.channel.send("오늘은 예정된 스크림이 없습니다")
                return

            # 스크림 신청
            ws = await get_spreadsheet('current_scream_list')
            try:
                ws.find(author.mention)
            except:
                ws.append_row([author.mention])
                await message.channel.send("스크림 신청이 완료되었습니다")
                return

            await message.channel.send("이미 신청되었습니다 >>스크림으로 명단에서 본인 이름을 확인하세요")
            return

        if content == "스크림신청취소":
            # 예정된 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is True:
                await message.channel.send("오늘은 예정된 스크림이 없습니다")
                return

            # 스크림 신청 취소
            ws = await get_spreadsheet('current_scream_list')
            try:
                ws.find(author.mention)
            except:
                await message.channel.send("신청되지 않은 참가자입니다.")
                return

            cell = ws.find(author.mention)
            row = cell.row
            ws.delete_rows(row)

            await message.channel.send("스크림 신청 취소가 완료되었습니다")
            return

        if content == "스크림":
            # 예정된 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is True:
                await message.channel.send("오늘은 예정된 스크림이 없습니다")
                return

            # 스크림 정보를 보여주기 위한 작업
            ws = await get_spreadsheet('current_scream')

            opener = ws.cell(1, 1).value
            time = ws.cell(2, 1).value
            limit = ws.cell(3, 1).value
            desc = ws.cell(4, 1).value

            ws = await get_spreadsheet('current_scream_list')
            participant = ws.col_values(1)

            # list에 \n 추가
            for index, value in enumerate(participant):
                number = index + 1
                participant[index] = str(number) + '. ' + participant[index] + '\n'

            # list to string and replace "," to ""
            participant = ','.join(participant)
            participant = participant.replace(",", "")

            counts = ws.row_count

            embed = discord.Embed(title="오늘의 스크림", description=desc, color=12745742)
            embed.add_field(name="시간", value=time, inline=False)
            embed.add_field(name="제한 인원", value=limit, inline=False)
            embed.add_field(name="개최자", value=opener, inline=False)
            embed.add_field(name="참가자 {}명".format(counts), value=participant, inline=False)

            await channel.send(embed=embed)
            return

        if content.startswith("개최자변경"):
            # 예정된 스크림이 있는지 확인
            print("개최자 변경")
            result = await is_spreadsheet_empty('current_scream')
            # is empty
            if result is True:
                await message.channel.send("오늘은 예정된 스크림이 없습니다")
                return

            # 새로운 개최자로 변경
            newopener = content.split(" ")[1]

            ws = await get_spreadsheet('current_scream')
            ws.update_cell(1, 1, newopener)
            await message.channel.send("개최자 업데이트 완료")
            return

        if content.startswith("시간변경"):
            # 예정된 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is True:
                await message.channel.send("오늘은 예정된 스크림이 없습니다")
                return

            # 새로운 시간으로 업데이트
            newtime = content.split(" ")[1]

            ws = await get_spreadsheet('current_scream')
            ws.update_cell(2, 1, newtime)
            await message.channel.send("시간 업데이트 완료")
            return

        if content.startswith("제한인원변경"):
            # 예정된 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is True:
                await message.channel.send("오늘은 예정된 스크림이 없습니다")
                return

            # 새로운 시간으로 업데이트
            newlimit = content.split(" ")[1]

            ws = await get_spreadsheet('current_scream')
            ws.update_cell(3, 1, newlimit)
            await message.channel.send("제한 인원 업데이트 완료")
            return

        if content == "스크림종료":
            # 종료할 스크림이 있는지 확인
            result = await is_spreadsheet_empty('current_scream')
            if result is True:
                await message.channel.send("종료할 스크림이 없습니다")
                return

            # 종료 커맨드 날린 author 가 개최자 혹은 운영자인지 확인
            if author.mention != (await get_opener(author.mention)) and (not is_moderator(author)):
                await message.channel.send("내전 개최자 또는 운영진만 내전을 종료할 수 있습니다.")
                return

            # 스크림 종료하는 작업 준비
            ws = await get_spreadsheet('current_scream')
            ws.clear()
            ws.resize(rows=4, cols=1)

            ws = await get_spreadsheet('current_scream_list')
            ws.resize(rows=1, cols=1)
            ws.clear()

            await message.channel.send("@everyone \n 스크림이 종료되었습니다")
            return

        if content == "하랑봇":
            embed = discord.Embed(title=":robot:하랑봇:robot:", description="하랑봇 ver1.4 온라인!", color=3066993)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/708306592465944591/723914634116988988/3b53af51b6da75d2.png")
            await channel.send(embed=embed)
            return

        if content == "한줄소개":
            spreadsheet = await get_spreadsheet('responses1')
            data = spreadsheet.col_values(3)
            data[0] = "한줄소개 명령어 리스트입니다!"
            await channel.send(data)
            return

        if content == "명령어":
            embed = discord.Embed(title="명령어 모음", description="하랑봇 문의사항은 Bewhy에게 전달해주세요", color=12745742)
            embed.add_field(name="LINK for Everything", value="문의방, 수다방, 공지방, 하랑카페, 신입안내", inline=False)
            embed.add_field(name="운영진 및 스탭 목록", value="운영진", inline=False)
            embed.add_field(name="스크림", value="스크림개최 HH:MM 제한인원 설명, 스크림종료, 스크림신청, 스크림신청취소,\n스크림, 시간변경 HH:MM, 개최자변경 @멘션, 제한인원변경 N", inline=False)
            embed.add_field(name="Utility", value="참여코드, 로또, 주사위, 맵추천, 공수추천, 팀편성, 내전팀편성, 한줄소개, 한줄소개설문지", inline=False)
            await channel.send(embed=embed)
            return

        if content == "운영진":
            spreadsheet = await get_spreadsheet('staff')
            data = spreadsheet.get_all_values()
            log = '\n\n'.join(map(lambda x: '\n'.join([t for t in x if t != '']), data))
            embed = discord.Embed(title=":fire: 운영진 목록\n", description=log, color=12320855)
            await channel.send(embed=embed)
            return

        if content == "문의방":
            # await message.channel.send("https://open.kakao.com/o/g233VUcb")
            embed = discord.Embed(title="문의방", description="문의방을 두려워하지 말라! \n https://open.kakao.com/o/gQIfr9pd",
                                  color=0xE86222)
            await channel.send(embed=embed)
            return

        if content == "수다방":
            await message.channel.send("https://open.kakao.com/o/goxpJxT")
            return

        if content == "공지방":
            await message.channel.send("https://open.kakao.com/o/gTJbLxT")
            return

        if content == "하랑카페":
            await message.channel.send("https://cafe.naver.com/owgreen")
            return

        if content == "신입안내":
            embed = discord.Embed(title="신입클랜원 안내 링크", description= "신입클랜원분들은 해당 사항 한 번씩 읽어주세요!!", color=0xFF5733)
            embed.add_field(name="디스코드 안내 링크", value="https://cafe.naver.com/owgreen/10272", inline=False)
            embed.add_field(name="하랑 신입클랜원 안내 링크", value="https://cafe.naver.com/owgreen/10861", inline=False)
            await channel.send(embed=embed)
            return
         
        if content == "참여코드":
            await message.channel.send("수다방/공지방 : 1207")
            return                  

        if content == "한줄소개설문지":
            await message.channel.send("https://forms.gle/no8sPtEtG1fsKJ2G9")
            return

        if content == "주사위":
            dice = "0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 5 5 5 5 5 5 5 6 6 6 6 6 6 777"
            dicechoice = dice.split(" ")
            dicenumber = random.randint(1, len(dicechoice))
            print(len(dicechoice))
            print(dicenumber)
            diceresult = dicechoice[dicenumber - 1]
            await message.channel.send("오늘 당신의 주사위는....!  **||   " + diceresult + "   ||**!!!!")
            return

        if content == "로또":
            lotteryNumbers = []

            for i in range(0, 6):
                number = random.randint(1, 45)
                while number in lotteryNumbers:
                    number = random.randint(1, 45)
                lotteryNumbers.append(number)

            lotteryNumbers.sort()
            lotto = ' '.join(map(str, lotteryNumbers))
            await message.channel.send("Good luck!\n" + lotto)
            return

        if content == "맵추천":
            # 파리 호라이즌
            maps = "네팔 리장타워 부산 오아시스 일리오스 볼스카야인더스터리 아누비스신전 하나무라 66번국도 감시기지:지브롤터 도라도 리알토 쓰레기촌 하바나 눔바니 블리자드월드 아이헨발데 왕의길 할리우드"
            mapchoice = maps.split(" ")
            mapnumber = random.randint(1, len(mapchoice))
            mapresult = mapchoice[mapnumber - 1]
            await message.channel.send("하랑봇이 추천드리는 오늘의 맵은....!  **||" + mapresult + "||**")
            return

        if content == "공수추천":
            choices = "공격이 수비가"
            choice = choices.split(" ")
            number = random.randint(1, len(choice))
            result = choice[number - 1]
            await message.channel.send("나는요 " + result + " 좋은거헐! (짝짝) 오또케!")
            return

        # 내전 팀편성
        if content.startswith("내전팀편성"):
            team1List = []
            team2List = []

            if len(content.split(" ")) != 13 and len(content.split(" ")) != 15:
                    data = "잘못 입력한 부분이 있습니다. 다시 입력해주세요."
                    await channel.send(data)
                    return
            if len(content.split(" ")) == 13:
                for idx in range(1, 13):
                    if idx < 7:
                        team1List.append(content.split(" ")[idx])
                    else:
                        team2List.append(content.split(" ")[idx])

                embed = discord.Embed(title="오늘의 내전 팀편성", description="해당 명령어 문의사항은 Bewhy에게 전달해주세요", color=0xFF5733)
                embed.add_field(name="1팀", value="[탱커] "+team1List[0]+"\t"+team1List[1]+"\n[딜러] "+team1List[2]+"\t"+team1List[3]+"\n[힐러] "+team1List[4]+"\t"+team1List[5], inline=False)
                embed.add_field(name="2팀", value="[탱커] "+team2List[0]+"\t"+team2List[1]+"\n[딜러] "+team2List[2]+"\t"+team2List[3]+"\n[힐러] "+team2List[4]+"\t"+team2List[5], inline=False)
                await channel.send(embed=embed)
                return

            if len(content.split(" ")) == 15:
                for idx in range(3, 15):
                    if idx < 9:
                        team1List.append(content.split(" ")[idx])
                    else:
                        team2List.append(content.split(" ")[idx])

                embed = discord.Embed(title="오늘의 내전 팀편성", description="해당 명령어 문의사항은 Bewhy에게 전달해주세요", color=0xFF5733)
                embed.add_field(name=content.split(" ")[1], value="[탱커] "+team1List[0]+"\t"+team1List[1]+"\n[딜러] "+team1List[2]+"\t"+team1List[3]+"\n[힐러] "+team1List[4]+"\t"+team1List[5], inline=False)
                embed.add_field(name=content.split(" ")[2], value="[탱커] "+team2List[0]+"\t"+team2List[1]+"\n[딜러] "+team2List[2]+"\t"+team2List[3]+"\n[힐러] "+team2List[4]+"\t"+team2List[5], inline=False)
                await channel.send(embed=embed)
                return

        spreadsheet = await get_spreadsheet('responses1')
        roles = spreadsheet.col_values(6)
        battletags = spreadsheet.col_values(2)

        nickname = spreadsheet.col_values(3)

        try:
            index = nickname.index(content) + 1
        except gspread.exceptions.CellNotFound:
            return
        except gspread.exceptions.APIError:
            return

        # mention = spreadsheet.cell(index, 1).value
        battletag = spreadsheet.cell(index, 2).value
        link = spreadsheet.cell(index, 4).value
        description = spreadsheet.cell(index, 5).value
        thumbnaillink = spreadsheet.cell(index, 6).value
        imagelink = spreadsheet.cell(index, 7).value
        league = spreadsheet.cell(index, 8).value
        print(index, battletag, link, description, imagelink, thumbnaillink, league)

        member = await get_member_by_battletag(battletag)
        if member is None:
            print("none")
            return
        elif await has_role(member, "마스터"):
            role = "마스터"
            roleimage = ":pen_ballpoint:"
        elif await has_role(member, "운영진"):
            role = "운영진"
            roleimage = ":construction_worker:"
        elif await has_role(member, "스텝-디자인"):
            role = "디자인 스텝"
            roleimage = ":woman_construction_worker:"
        elif await has_role(member, "스텝-DC"):
            role = "디스코드 스텝"
            roleimage = ":woman_construction_worker:"
        elif await has_role(member, "클랜원"):
            role = "클랜원"
            roleimage = ":boy:"
        elif await has_role(member, "신입 클랜원"):
            role = "신입 클랜원"
            roleimage = ":baby:"
        else:
            return

        embed = discord.Embed(title="한줄소개", description=description, color=3447003)

        if link is not '':
            embed = discord.Embed(title="바로가기", url=link, description=description, color=3447003)

        # embed.content(name=battletag)

        if league is not '':
            embed.add_field(name="League", value=":trophy: 제" + league + "회 우승", inline=False)
        embed.add_field(name="직책", value=roleimage + role, inline=True)
        if imagelink is not '':
            embed.set_image(url=imagelink)
        if thumbnaillink is not '':
            embed.set_thumbnail(url=thumbnaillink)

        await channel.send(embed=embed)






access_token = os.environ["BOT_TOKEN"]
client.run(access_token)



