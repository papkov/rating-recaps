import unittest
from app import invitation


class RecapsTests(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)

    def test_get_invitation(self):
        r = invitation.get_invitation(team_id=3423,
                                      invitation_id=21,
                                      position='ректору',
                                      university='Федерального государственного образовательного бюджетного учреждения '
                                                 'высшего образования',
                                      first_name='Иван',
                                      second_name='Иванови',
                                      surname='Иванову',
                                      team_name='Название команды',
                                      recaps=["Игрок 1, группа",
                                              "Игрок 2, группа",
                                              "Игрок 3, группа"
                                              ])
        self.assertTrue(r)


if __name__ == '__main__':
    unittest.main()
