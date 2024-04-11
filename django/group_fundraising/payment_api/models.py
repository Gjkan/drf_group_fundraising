from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.timezone import now


class Collect(models.Model):
    class Meta():
        verbose_name = 'Групповой денежный сбор'
        verbose_name_plural = 'Групповые денежные сборы'
        
    OCCASION_CHOICES = [
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('charity', 'Благотворительность'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор группового денежного сбора')
    name = models.CharField(max_length=200, verbose_name='Название группового денежного сбора')
    occasion = models.CharField(max_length=2000, verbose_name='Повод группового денежного сбора',
                                choices=OCCASION_CHOICES, default=OCCASION_CHOICES[0][0])
    description = models.CharField(max_length=2000, verbose_name='Описание группового денежного сбора')
    aim_sum = models.IntegerField(verbose_name='Цель группового денежного сбора, р', default=0)
    infinity_sum = models.BooleanField(verbose_name='Флаг бесконечного сбора', default=False)
    current_sum = models.IntegerField(verbose_name='Собранная сумма в данный момент, р', default=0)
    number_of_people = models.IntegerField(verbose_name='Количество людей, участвующих в групповом денежном сборе',
                                           default=0)
    collect_cover = models.ImageField(verbose_name='Обложка группового денежного сбора', null=True, blank=True)
    finish_collect_date_time = models.DateTimeField(verbose_name='Дата завершения сбора', default=now)
    collect_lent = models.TextField(verbose_name='Лента сбора', default='')

    def change_collect_lent(self, payment, operation, old_pay=None):
        """Method changes collect_lent depends of operation with payment
           and user information"""
        
        first_name = payment.user.first_name
        last_name = payment.user.last_name
        if first_name and last_name:
            self.collect_lent += f'{first_name} {last_name}'
        else:
            self.collect_lent += payment.user.username

        if operation == 'create':
            self.collect_lent += f' внёс/внесла пожертвование {payment.payment} р. Спасибо!\n'
        elif operation == 'delete':
            self.collect_lent += f' удалил/удалила пожертвование {payment.payment} р. Бывает!\n'
        elif operation == 'update':
            self.collect_lent += f' удалил/удалила пожертвование {old_pay} р ' \
                                 f'и внёс/внесла {payment.payment} р. Спасибо!\n'

    def change_number_of_people(self):
        """Method changes number_of_people by counting unique
           users, which made payments related that collect"""
        self.number_of_people = Payment.objects.filter(collect=self).values('user').distinct().count()

    def update_collect_before_delete_payment(self, payment):
        """Method for updating collect_lent and number_of_people
           right before payment deleting"""
        self.current_sum -= payment.payment
        self.change_collect_lent(payment=payment, operation='delete')
        self.change_number_of_people()
        self.save()
    
    def update_collect_after_payment_creation(self, payment):
        """Method for updating collect_lent and number_of_people
           right after payment was create"""
        self.current_sum += payment.payment
        self.change_collect_lent(payment=payment, operation='create')
        self.change_number_of_people()
        self.save()
    
    def update_collect_after_update_payment(self, payment, old_pay):
        """Method for updating collect_lent and number_of_people
           right after payment was update"""
        self.current_sum += (payment.payment - old_pay)
        if old_pay != payment.payment:
            self.change_collect_lent(payment=payment, operation='update', old_pay=old_pay)
        self.change_number_of_people()
        self.save()

    def __str__(self):
        return f'{self.name} {self.author} {self.aim_sum}'


class Payment(models.Model):
    class Meta():
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE, verbose_name='Групповой денежный сбор', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь донатер')
    payment = models.IntegerField(verbose_name='Сумма платежа, р')

    def can_delete(self):
        """Method checks, can user delete payment of not.
           Logics - if collect ended, payment is not deletable"""
        if self.collect:
            return now() < self.collect.finish_collect_date_time
        return False

    def can_update(self):
        """Method checks, can user update payment of not.
           Logics - if collect ended, payment is not updatable"""
        return self.can_delete()
    

    def __str__(self):
        return str(self.payment)
