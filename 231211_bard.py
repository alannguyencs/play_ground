"""
Installation:

BardAPI: pip install bardapi==0.1.23a
Reference: https://pypi.org/project/bardapi/

How to get session_id: please see the tutorial at https://www.youtube.com/watch?v=kT8Q7aIlgy0&ab_channel=KNOWLEDGEDOCTOR

"""

from bardapi import Bard
import secret

Barder = Bard(secret.bard_session_id)


response = Barder.get_answer("Please give me the history of company Detalytics in Singapore, like which year established, who the founder is?")['content']
print(response)