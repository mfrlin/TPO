from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.coupon.views',
	url(r'^mycoupons/$', 'mycoupons', name='mycoupons'),
	url(r'^mycoupons/add$', 'add', name='addcoupon'),
	url(r'^mycoupons/edit/(?P<id>\d+)$', 'edit', name='editcoupon'),
	url(r'^mycoupons/manage$', 'manage', name='managecoupon'),
	url(r'^mycoupons/manageall$', 'manageall', name='manageall'),
	url(r'^mycoupons/csvupload$', 'csv_upload', name='csvupload'),
)
