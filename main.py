import discord
import random
import asyncio
import time

client = discord.Client()

token = 'Token'


def embed(title, description):
    embed = discord.Embed(title=title, description=description, color=0xFF80ED)
    return embed


@client.event
async def on_connect():
    while True:
        await client.change_presence(activity=discord.Streaming(name=f"{len(client.guilds)}개의 서버에서 사용중", url='https://www.twitch.tv/lazini_boardgame'))


@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    if msg.content == '!hellothisisverification':
        await msg.channel.send('Supporter#1111(919201547857055806)')

    if msg.content == '!도움말':

        msgs = '''
        !다빈치 (@함께 플레이 할 유저 멘션)

        다빈치 코드 플레이 방법

        * 카드 리스트 *

        [ 검정 ]
        - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

        [ 흰색 ]
        - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

        1. 먼저 봇이 패를 섞고 `정렬`된 상태로 4장식 분배합니다.

        2. 상대방이 가지고있는 패의 색깔이 공개되며 `!다빈치 멘션`을 입력한 유저부터 턴이 시작됩니다.

        3. 매턴 남은 카드에서 한장씩 카드가 주어집니다.

        4. 본인에게 배분된 패와 상대방 패의 색깔을 보며 상대방의 패를 알아맞춥니다.

        5. (맞추려는번호순서) (맞추려는번호) (맞추려는색깔) 을 입력하여 맞출 수 있습니다. 띄어쓰기를빼먹거나 추가적으로 하면 에러가 발생할 수도 있습니다.

        6. 만약 상대방의 패를 맞춘다면 계속하여 맞출 수 있는 기회가 주어지며, 맞출때마다 상대방은 패 하나를 까게됩니다.

        7. 만약 상대방의 패를 못맞췄다면 `3`번에 주어진 카드가 까집니다.

        8. 까진 카드와 까지지 않은 카드 수가 동일하다면 그 사람은 패배합니다.

        9. 그 이외에도 5분 제한시간, 더이상 남은카드가 없을 시, 게임은 종료됩니다.
        '''
        await msg.channel.send(embed=embed('다빈치코드 도움말', msgs))

    if msg.content.startswith('!다빈치 '):
        i = 0
        for channel in msg.guild.channels:
            if str(channel.name) == str(msg.author.id):
                i = 1
                break

        if i == 1:
            return await msg.channel.send(embed=embed('이미 채널이 존재합니다', '이미 생성된 놀이채널이 있어요!\n관리자에게 문의해주세요!'))

        try:
            mention = msg.mentions[0].id
            if mention == msg.author.id:
                raise TypeError

            if mention == client.user.id:
                raise TypeError
        except:
            return await msg.channel.send(embed=embed('사용법 안내', '다빈치코드를 플레이하려면 !다빈치 @멘션을 입력해주세요.'))

        await msg.channel.send(embed=embed('요청 전송 완료', f'<@{str(mention)}>님에게 다빈치 코드 플레이 요청을 보내셨어요!'))

        try:
            player1 = await client.fetch_user(int(mention))
            await player1.send(embed=embed('다빈치 코드', f'<@{str(msg.author.id)}>님이 다빈치 코드 플레이 요청을 보내셨어요!\n플레이하시려면 !승인을, 거부하시려면 !거절을 입력해주세요!'))
        except:
            return await msg.channel.send('상대방이 마음의 문을 닫고 메세지를 받지 않아요 ㅜㅜ')

        try:
            answer = await client.wait_for('message', timeout=60, check=lambda m: isinstance(m.channel, discord.DMChannel) and int(m.author.id) == int(mention) and (m.content == '!승인' or m.content == '!거절'))
        except:
            return await msg.channel.send(embed=embed('시간 지남', '상대방이 마음의 문을 닫고 응답하지 않아요 ㅜㅜ'))

        if answer.content == '!거절':
            await answer.author.send(embed=embed('거절 완료', '거절되었습니다!'))
            return await msg.channel.send(embed=embed('거절됨', '상대방이 거절했습니다!'))
        else:

            overwrites = {
                msg.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                msg.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                answer.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            try:
                channel = await msg.guild.create_text_channel(str(msg.author.id), overwrites=overwrites)
            except:
                return await msg.channel.send('놀이 채널을 만들 수 없습니다!\n봇에게 권한을 부여해주세요.')
            await answer.author.send(embed=embed('채널 생성됨', f'<#{str(channel.id)}> 로 이동해주세요!'))
            await msg.channel.send(embed=embed('채널 생성됨', f'<#{str(channel.id)}> 로 이동해주세요!'))

            await channel.send(embed=embed('패 섞는중...', '일단 패를 뽑을게요!\n잠시 기다려주세요\n아 참고로 이 게임은 조커가 없답니다!'))

            await asyncio.sleep(5)

            items = [
                [0, '검'],
                [1, '검'],
                [2, '검'],
                [3, '검'],
                [4, '검'],
                [5, '검'],
                [6, '검'],
                [7, '검'],
                [8, '검'],
                [9, '검'],
                [10, '검'],
                [11, '검'],
                [0, '흰'],
                [1, '흰'],
                [2, '흰'],
                [3, '흰'],
                [4, '흰'],
                [5, '흰'],
                [6, '흰'],
                [7, '흰'],
                [8, '흰'],
                [9, '흰'],
                [10, '흰'],
                [11, '흰'],
            ]
            random.shuffle(items)

            player1 = []
            player2 = []

            for i in range(4):
                pick = random.choice(items)
                items.remove(pick)
                player1.append(pick)

            for i in range(4):
                pick = random.choice(items)
                items.remove(pick)
                player2.append(pick)

            player1 = [[int(x[0]), x[1]] for x in player1]
            player1.sort()

            player1_card = [f'{x[0]} {x[1]}' for x in player1]
            player1_card = ' | '.join(player1_card)
            print(player1_card)
            player1_hit = []

            player2 = [[int(x[0]), x[1]] for x in player2]
            player2.sort()
            print(player2)
            player2_card = [f'{x[0]} {x[1]}' for x in player2]
            player2_card = ' | '.join(player2_card)
            player2_hit = []

            await msg.author.send(embed=embed('패 설정 완료', f'<@{msg.author.id}>님의 패 입니다.\n{player1_card}'))
            await answer.author.send(embed=embed('패 설정 완료', f'<@{answer.author.id}>님의 패 입니다.\n{player2_card}'))
            await channel.send('자 패가 다 뽑아졌습니다.\n게임을 시작해볼까요?')
            start = time.time()
            while not (len(player1) <= len(player1_hit)) and not (len(player2) <= len(player2_hit)) and not len(items) == 0:
                end = time.time()
                if (start - end >= 300):
                    break

                pick = random.choice(items)
                items.remove(pick)
                player1.append(pick)
                player1_win = 0
                while player1_win == 0:

                    player1 = [[int(x[0]), x[1]] for x in player1]
                    player2 = [[int(x[0]), x[1]] for x in player2]
                    player1.sort()
                    player2.sort()

                    await msg.author.send(embed=embed('설명서 1', f'<@{msg.author.id}>님 차례네요.\n디엠으로 상대방의 맞출 패를 입력해주세요\n당신의 카드를 상대가 `{len(player1) - len(player1_hit)}`장 맞추시면 이깁니다!\n상대방의 카드를 `{len(player2) - len(player2_hit)}`장 맞추시면 이깁니다!\n제한시간 `60`초 드립니다.'))
                    temp1 = []
                    for n, i in zip(range(len(player2)), player2):
                        print(str(i[0]) + ' ' + str(i[1]))
                        if str(i[0]) + ' ' + str(i[1]) in player2_hit:
                            temp1.append(f'{n}번 : `({str(i[0])} - {i[1]})`')
                        else:
                            temp1.append(f'{n}번 : ? 🃁 {i[1]}')
                    cards = '\n'.join(temp1)
                    await msg.author.send(embed=embed('설명서 2', f'현재 <@{answer.author.id}>님의 카드\n카드 번호를 양식에 맞춰 입력해주세요! \n양식: 번호 코드번호 색깔\n예시: `1 11 검`\n{cards}'))
                    player1_end = 0
                    try:
                        player1_answer = await client.wait_for('message', timeout=60, check=lambda m: isinstance(m.channel, discord.DMChannel) and int(m.author.id) == int(msg.author.id))
                    except:
                        await channel.send(embed=embed('잠수함 탐지!', f'<@{msg.author.id}>님이 반응이 없어 다음턴으로 넘어갑니다!'))
                        player1_end = 1

                    if not player1_end == 1:
                        try:
                            player1_answers = player1_answer.content.split(' ')
                        except:
                            await channel.send(embed=embed('면접에도 서류 양식 안맞춰오면 탈락이잖아요!', f'<@{msg.author.id}>님이 올바른 양식을 입력하지 않아 다음턴으로 넘어갑니다!'))
                            player1_end = 1

                        if not player1_end == 1:

                            if not player1_answers[0].isdigit():
                                await channel.send(embed=embed('면접에도 서류 양식 안맞춰오면 탈락이잖아요!', f'<@{msg.author.id}>님이 올바른 양식을 입력하지 않아 다음턴으로 넘어갑니다!'))
                                player1_end = 1
                            else:
                                if not player1_end == 1:
                                    try:
                                        card = str(
                                            player1_answers[1]) + ' ' + str(player1_answers[2])
                                        if str(player2[int(player1_answers[0])][0]) + ' ' + player2[int(player1_answers[0])][1] == str(card):
                                            await msg.author.send(embed=embed('패 설정 완료', f'<@{msg.author.id}>님의 패 입니다.\n{player1_card}'))
                                            await answer.author.send(embed=embed('상대.. 좀 치는놈인가..?', f'상대방이 맞추셨어요!\n<@{answer.author.id}>님의 {player1_answers[0]}번째 카드는 {card}이였어요!'))
                                            await msg.author.send(embed=embed('오.. 좀 치네 ㅋㅋ', f'맞추셨어요!\n<@{answer.author.id}>님의 {player1_answers[0]}번째 카드는 {card}이였어요!'))
                                            # player2.remove(card)
                                            player2_hit.append(card)
                                            player2_card = [
                                                f'{x[0]} {x[1]}' for x in player2]
                                            player2_card = ' | '.join(
                                                player2_card)
                                    except:
                                        await channel.send(embed=embed('면접에도 서류 양식 안맞춰오면 탈락이잖아요!', f'<@{msg.author.id}>님이 올바른 양식을 입력하지 않아 다음턴으로 넘어갑니다!'))

                                    else:
                                        await answer.author.send(embed=embed('다행이다!', f'상대방이 못맞추셨어요!'))
                                        await msg.author.send(embed=embed('아깝당 ㅜㅜ', f'못맞추셨어요!'))
                                        # player1.remove(pick)
                                        player1_hit.append(pick)
                                        player1_card = [
                                            f'{x[0]} {x[1]}' for x in player1]
                                        player1_card = ' | '.join(player1_card)
                                        player1_win = 1

                pick = random.choice(items)
                items.remove(pick)
                player2.append(pick)

                player2_win = 0
                while player2_win == 0:

                    player1 = [[int(x[0]), x[1]] for x in player1]
                    player2 = [[int(x[0]), x[1]] for x in player2]
                    player1.sort()
                    player2.sort()

                    await answer.author.send(embed=embed('설명서 1', f'<@{answer.author.id}>님 차례네요.\n디엠으로 상대방의 맞출 패를 입력해주세요\n당신의 카드를 상대가 `{len(player2) - len(player2_hit)}`장 맞추시면 이깁니다!\n상대방의 카드를 `{len(player1) - len(player1_hit)}`장 맞추시면 이깁니다!\n제한시간 `60`초 드립니다.'))
                    temp1 = []
                    for n, i in zip(range(len(player1)), player1):
                        if str(i[0]) + ' ' + str(i[1]) in player1_hit:
                            temp1.append(f'{n}번 : `({str(i[0])} - {i[1]})`')
                        else:
                            temp1.append(f'{n}번 : ? 🃁 {i[1]}')
                    cards = '\n'.join(temp1)
                    await answer.author.send(embed=embed('설명서 2', f'현재 <@{msg.author.id}>님의 카드\n카드 번호를 양식에 맞춰 입력해주세요! \n양식: (번호) 코드번호 색깔\n예시: `1 11 검`\n{cards}'))
                    player2_end = 0
                    try:
                        player2_answer = await client.wait_for('message', timeout=60, check=lambda m: isinstance(m.channel, discord.DMChannel) and int(m.author.id) == int(answer.author.id))
                    except:
                        await channel.send(embed=embed('잠수함 탐지', f'<@{answer.author.id}>님이 반응이 없어 다음턴으로 넘어갑니다!'))
                        player2_end = 1

                    if not player2_end == 1:
                        try:
                            player2_answers = player2_answer.content.split(' ')
                            test = str(player1[int(player2_answers[0])][0]) + \
                                ' ' + player1[int(player2_answers[0])][1]
                        except:
                            await channel.send(embed=embed('면접에서도 서류 양식 틀리면 탈락이잖아요!', f'<@{answer.author.id}>님이 올바른 양식을 입력하지 않아 다음턴으로 넘어갑니다!'))
                            player2_end = 1

                        if not player2_end == 1:

                            if not player2_answers[0].isdigit():
                                await channel.send(embed=embed('면접에서도 서류 양식 틀리면 탈락이잖아요!', f'<@{answer.author.id}>님이 올바른 양식을 입력하지 않아 다음턴으로 넘어갑니다!'))
                                player2_end = 1
                            else:
                                if not player2_end == 1:
                                    try:
                                        card = str(
                                            player2_answers[1]) + ' ' + str(player2_answers[2])
                                        if str(player1[int(player2_answers[0])][0]) + ' ' + player1[int(player2_answers[0])][1] == str(card):
                                            await answer.author.send(embed=embed('패 설정 완료', f'<@{answer.author.id}>님의 패 입니다.\n{player2_card}'))
                                            await msg.author.send(embed=embed('오.. 좀 치는놈인가..?', f'상대방이 맞추셨어요!\n<@{msg.author.id}>님의 {player2_answers[0]}번째 카드는 {card}이였어요!'))
                                            await answer.author.send(embed=embed('오.. 좀 치네 ㅋㅋ', f'맞추셨어요!\n<@{msg.author.id}>님의 {player2_answers[0]}번째 카드는 {card}이였어요!'))
                                            # player1.remove(card)
                                            player1_hit.append(card)
                                            player1_card = [
                                                f'{x[0]} {x[1]}' for x in player1]
                                            player1_card = ' | '.join(
                                                player1_card)
                                    except:
                                        await channel.send(embed=embed('면접에서도 서류 양식 틀리면 탈락이잖아요!', f'<@{answer.author.id}>님이 올바른 양식을 입력하지 않아 다음턴으로 넘어갑니다!'))

                                    else:
                                        await msg.author.send(embed=embed('좋았어!', f'상대방이 못맞추셨어요!'))
                                        await answer.author.send(embed=embed('까비 ㅠㅠ', f'못맞추셨어요!'))
                                        # player2.remove(pick)
                                        player2_hit.append(pick)
                                        player2_card = [
                                            f'{x[0]} {x[1]}' for x in player2]
                                        player2_card = ' | '.join(player2_card)
                                        player2_win = 1

                player1 = [[int(x[0]), x[1]] for x in player1]
                player2 = [[int(x[0]), x[1]] for x in player2]
                player1.sort()
                player2.sort()

                await msg.author.send(embed=embed('패 추가 완료', f'<@{msg.author.id}>님의 패 입니다.\n{player1_card}'))
                await answer.author.send(embed=embed('패 추가 완료', f'<@{answer.author.id}>님의 패 입니다.\n{player2_card}'))

            if len(player1) == len(player1_hit):
                await channel.send(embed=embed('오늘밤 주인공은 누굴까?', f'<@{answer.author.id}>님이 승리하셨습니다.'))
                await answer.author.send(embed=embed('오늘밤 주인공은 누굴까?', f'<@{answer.author.id}>님이 승리하셨습니다.'))
                await msg.author.send(embed=embed('두둥탁!', f'<@{answer.author.id}>님이 승리하셨습니다.'))
                await asyncio.sleep(5)
                try:
                    await channel.delete()
                except:
                    return await channel.send('채널을 삭제할 수 없습니다.\n봇에게 권한을 부여해주세요!')
            elif len(player2) == len(player2_hit):
                await channel.send(embed=embed('오늘밤 주인공은 누굴까?', f'<@{msg.author.id}>님이 승리하셨습니다.'))
                await answer.author.send(embed=embed('오늘밤 주인공은 누굴까?', f'<@{msg.author.id}>님이 승리하셨습니다.'))
                await msg.author.send(embed=embed('두둥탁!', f'<@{msg.author.id}>님이 승리하셨습니다.'))
                await asyncio.sleep(5)
                try:
                    await channel.delete()
                except:
                    return await channel.send('채널을 삭제할 수 없습니다.\n봇에게 권한을 부여해주세요!')
            elif (start - time.time() >= 300):
                await answer.author.send(embed=embed('너무 오~~래걸린다 ㅠㅠ', f'시간이 너무 오래걸려요! 제한시간은 딱 5분! 저두 바쁘기 때문에.. 아무튼 무승부입니다!\n치열한 게임이었네요.'))
                await msg.author.send(embed=embed('너무 오~~래걸린다 ㅠㅠ', f'시간이 너무 오래걸려요! 제한시간은 딱 5분! 저두 바쁘기 때문에.. 아무튼 무승부입니다!\n치열한 게임이었네요.'))
                await channel.send(embed=embed('너무 오~~래걸린다 ㅠㅠ', f'시간이 너무 오래걸려요! 제한시간은 딱 5분! 저두 바쁘기 때문에.. 아무튼 무승부입니다!\n치열한 게임이었네요.'))
                await asyncio.sleep(5)
                try:
                    await channel.delete()
                except:
                    return await channel.send('채널을 삭제할 수 없습니다.\n봇에게 권한을 부여해주세요!')
            else:
                await answer.author.send(embed=embed('결국.. 승자는 없었다고 한다..', f'더이상 뽑을 카드가 없네요 ㅜㅜ 카드 좀 사오겠습니다 아무튼 무승부입니다!\n치열한 게임이었네요.'))
                await msg.author.send(embed=embed('결국.. 승자는 없었다고 한다..', f'더이상 뽑을 카드가 없네요 ㅜㅜ 카드 좀 사오겠습니다 아무튼 무승부입니다!\n치열한 게임이었네요.'))
                await channel.send(embed=embed('결국.. 승자는 없었다고 한다..', f'더이상 뽑을 카드가 없네요 ㅜㅜ 카드 좀 사오겠습니다 아무튼 무승부입니다!\n치열한 게임이었네요.'))
                await asyncio.sleep(5)
                try:
                    await channel.delete()
                except:
                    return await channel.send('채널을 삭제할 수 없습니다.\n봇에게 권한을 부여해주세요!')


client.run(token)
