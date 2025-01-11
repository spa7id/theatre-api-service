from django.test import TestCase
from django.core.exceptions import ValidationError
from theatre.models import (
    Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
)


class ActorModelTests(TestCase):
    def test_actor_str(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(str(actor), "John Doe")


class GenreModelTests(TestCase):
    def test_genre_str(self):
        genre = Genre.objects.create(name="Drama")
        self.assertEqual(str(genre), "Drama")


class PlayModelTests(TestCase):
    def test_play_str(self):
        play = Play.objects.create(title="Hamlet", description="A classic tragedy.")
        self.assertEqual(str(play), "Hamlet")


class TheatreHallModelTests(TestCase):
    def test_theatre_hall_capacity(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.assertEqual(hall.capacity, 200)

    def test_theatre_hall_str(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.assertEqual(str(hall), "Main Hall")


class PerformanceModelTests(TestCase):
    def setUp(self):
        self.play = Play.objects.create(title="Hamlet", description="A classic tragedy.")
        self.hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)

    def test_performance_str(self):
        performance = Performance.objects.create(play=self.play, theatre_hall=self.hall, show_time="2025-01-01 19:00")
        self.assertEqual(str(performance), "Hamlet - 2025-01-01 19:00:00")


class ReservationModelTests(TestCase):
    def test_reservation_str(self):
        reservation = Reservation.objects.create()
        self.assertTrue(str(reservation).startswith(str(reservation.created_at)))


class TicketModelTests(TestCase):
    def setUp(self):
        self.hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.play = Play.objects.create(title="Hamlet", description="A classic tragedy.")
        self.performance = Performance.objects.create(play=self.play, theatre_hall=self.hall, show_time="2025-01-01 19:00")
        self.reservation = Reservation.objects.create()

    def test_ticket_str(self):
        ticket = Ticket.objects.create(row=5, seat=10, performance=self.performance, reservation=self.reservation)
        self.assertEqual(str(ticket), "Hamlet - 2025-01-01 19:00:00 (row: 5, seat: 10)")

    def test_ticket_validation(self):
        ticket = Ticket(row=5, seat=10, performance=self.performance, reservation=self.reservation)
        ticket.full_clean()

        # Invalid ticket row
        invalid_ticket = Ticket(row=15, seat=10, performance=self.performance, reservation=self.reservation)
        with self.assertRaises(ValidationError):
            invalid_ticket.full_clean()

        invalid_ticket = Ticket(row=5, seat=25, performance=self.performance, reservation=self.reservation)
        with self.assertRaises(ValidationError):
            invalid_ticket.full_clean()
