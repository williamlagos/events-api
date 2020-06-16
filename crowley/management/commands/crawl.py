from django.core.management.base import LabelCommand, CommandError
from crowley.services import scrape_fb_page
from crowley.models import Crawler
from backend.models import Owner
from danceapp.settings import CROWLEY_LOGFILE
from pytz import timezone
from datetime import datetime
import sys


class Command(LabelCommand):
    help = 'Crawls on every active Owner Facebook page to harvest Events'

    # The maximum pages that will be fetched by a single Crawler at a time
    MAX_PAGES = 600

    def start_logging(self, filename):
        self.default_stdout = sys.stdout
        self.default_stderr = sys.stderr
        self.log_output = open(filename, 'w')
        sys.stdout = self.log_output
        sys.stderr = self.log_output

    def finish_logging(self):
        sys.stdout = self.default_stdout
        sys.stderr = self.default_stderr
        self.log_output.close()

    def handle_label(self, label, **options):
        if label != 'owner':
            raise CommandError('Unknown argument: "{}"'.format(label))

        self.start_logging(CROWLEY_LOGFILE)

        # Pega a lista de Crawlers ativos
        crawlers = Crawler.objects.filter(active=True)
        crawler_list = list(crawlers)
        num_crawlers = len(crawler_list)
        if num_crawlers == 0:
            raise CommandError('No active Crawlers were found.')

        # Pega a lista de Owners ativos
        owners = Owner.objects.filter(active=True)
        owners = owners.filter(owner_type=Owner.OWNER_TYPE_PAGE)
        if owners.count() == 0:
            raise CommandError('No active page Owners were found.')

        dt1 = datetime.now()
        current_page = 0
        current_crawler = 0

        self.stdout.write(
            self.style.SUCCESS('You summoned Crowley.')
        )
        self.stdout.write(
            self.style.SUCCESS('Now wait for the consequences...')
        )

        br_tz = timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)

        print('** Mr. Crowley was summoned at {}'.format(now.isoformat(' ')))
        print('* Started crawling {} owners'.format(owners.count()))
        print('* Using {} crawlers'.format(num_crawlers))

        print('- Crawling with {}...'.format(crawler_list[0].name))
        for owner in owners:
            crawler = crawler_list[current_crawler % num_crawlers]
            scrape_fb_page(owner.external_id, crawler.token)

            current_page += 1
            if current_page % self.MAX_PAGES == 0:
                current_crawler += 1
                crawler = crawler_list[current_crawler % num_crawlers]
                print('- Swapping to Crawler {} after {} pages.'.format(
                    crawler.name, current_page
                ))

        dt2 = datetime.now()
        delta = dt2 - dt1

        print('* Finished crawling {} pages'.format(current_page))
        print('* Ellapsed time: {} seconds.'.format(delta.total_seconds()))

        message = 'You waited for the longest {} seconds of your life.'
        self.stdout.write(
            self.style.SUCCESS(message.format(delta.total_seconds()))
        )

        self.finish_logging()
