# 익명투표
파이썬 Flask 프레임워크로 만들어진 간단한 익명투표 사이트입니다.

Flask, Flask-SQLAlchemy, Flask-wtf가 필요합니다.

## 사용법
1. 투표 관리자와 중계자를 믿을만한 사람으로 뽑습니다.
2. 투표 관리자가 서버에 설치하고 투표 주제를 설정합니다. 마스터키를 기억해 둡니다.
3. 투표 참가자들은 자신만의 랜덤 키를 정하고, 중계자에게 자신의 키를 알려줍니다.
4. 중계자는 이 키를 모아서 투표 관리자에게 전달합니다.
5. 투표 관리자가 마스터키를 이용해 이 키를 등록하면 투표가 시작됩니다.
6. 투표 참가자들은 자신의 키를 이용해 투표합니다.
7. 투표가 완료되면 투표 결과와 함께 정보가 공개됩니다.

## 믿을만한가요?
투표 관리자와 중계자가 결탁하는 경우가 아니라면 익명성과 깨끗한 투표 결과가 보장됩니다. 그러니까 믿을만한 사람으로 잘 뽑도록 합시다.

### 투표 관리자가 DB를 열어보는 경우
DB에 정보가 저장될 때 키와 선택의 대응 관계를 저장하지 않고, 누가 투표했는지와 어떤 선택을 했는지를 따로 저장합니다.
따라서 DB를 열어보더라도 누가 무엇을 골랐는지 바로 알 수 있는것은 아닙니다.

투표 관리자가 DB를 실시간으로 모니터링하고 있는 경우 어떤 키를 이용해 무엇에 투표했는지를 알아내는 것이 불가능하지는 않습니다.
하지만, 투표 관리자는 키의 목록만을 알고 어느 키가 누구의 것인지를 모르기 때문에 익명이 유지됩니다.

### 투표 관리자 또는 중계자가 다른 사람의 키를 사용하는 경우
투표 관리자와 중계자는 전체 키 목록을 알고 있기 때문에 다른 사람의 키로 투표하는 것이 가능합니다.
하지만 원래 그 키의 주인인 투표 참가자가 자신의 키를 사용하려고 했을 때 투표가 불가능하다는 메시지를 받기 때문에 확인할 수 있습니다. 

### 투표 결과를 조작하는 경우
투표 이후 자신이 몇 번째로 투표했는지, 어디에 투표했는지를 알려줍니다. 이 결과를 기억해 두었다가 최종 투표 결과와 비교해 투표 과정에 조작이 가해지지 않았는지 확인할 수 있습니다.
