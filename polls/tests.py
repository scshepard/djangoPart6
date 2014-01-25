import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

# Create your tests here.
def create_poll(question, days):
	"""
    Creates a poll with the given `question` published the given number of
    `days` offset to now (negative for polls published in the past,
    positive for polls that have yet to be published).
    """
	return Poll.objects.create(question=question,
		pub_date=timezone.now() + datetime.timedelta(days=days))
   
class PollMethodTests(TestCase):
	def test_index_view_with_no_polls(self):
		"""
		If no polls exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def text_index_view_with_a_past_poll(self):
		create_poll(question="Past poll.", days=-30)
		response = self.client.get(reverse('polls:index'))
		set.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll> Past poll.>']
			)

	def test_index_view_with_a_future_poll(self):
		create_poll(question="Future poll.",days=30)
		response=self.client.get(reverse('polls:index'))
		self.assertContains(response,"No polls are available.",status_code=200)
		self.assertQuerysetEqual(response.context['latest_poll_list'],[])

	def text_index_view_with_future_poll_and_past_poll(self):
		create_poll(question="Past poll.", days=-30)
		create_poll(question="Future poll.",days=30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll.>']
			)

	def test_index_view_with_two_past_polls(self):
		"""
		The polls index page may display multiple polls.
		"""
		create_poll(question="Past poll 1.", days=-30)
		create_poll(question="Past poll 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
		    response.context['latest_poll_list'],
		     ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
		)

	def test_was_published_recently_with_future_poll(self):
		future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(),False)

	def test_was_published_recently_width_old_poll(self):
		old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(old_poll.was_published_recently(),False)
		
	def test_was_published_recently_with_recent_poll(self):
		recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(), True)
