import redis
from django.conf import settings
from .models import Product

"""
zincrby，自增
zrange，按范围取
zunionstore，聚合存储
zrem，删除值
delete，删除key
"""

# 连接redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender:

    def get_product_key(self, id):
        # 一起购买的key
        return 'product:{}:purchased_with'.format(id)

    def get_purchased_key(self):
        # 购买的商品key
        return 'product:purchased'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # 找到与某个id一起购买的其他商品
                if product_id != with_id:
                    # 给一起购买的商品追加分数
                    r.zincrby(self.get_product_key(product_id),
                              amount=1,
                              value=with_id)
            # 自己本身加1
            r.zincrby(self.get_purchased_key(),
                        amount=1,
                        value=product_id)

    def get_best_saled(self, max_results=3):
        # 得到畅销商品id列表
        best_ids = r.zrevrange(self.get_purchased_key(), 0, -1)[:max_results]
        if best_ids:
            print(best_ids, Product.objects.filter(id__in=best_ids))
            best_products = list(Product.objects.filter(id__in=best_ids))

            # 得到商品id整数列表，并根据出现的顺序排序
            best_ids = [int(id) for id in best_ids]
            best_products.sort(key=lambda x: best_ids.index(x.id))
            print('按id索引排序：', best_products)
            return best_products
        else:
            return Product.objects.all()[:max_results]

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # 只有 1 product
            suggestions = r.zrange(
                             self.get_product_key(product_ids[0]),
                             0, -1, desc=True)[:max_results]
        else:
            # 生成临时的key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # 多个商品的缓存的keys，聚合，保存到临时key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # 删除推荐商品本身，得到其他被推荐的商品
            r.zrem(tmp_key, *product_ids)
            # 根据分数降序排列
            suggestions = r.zrange(tmp_key, 0, -1, 
                                   desc=True)[:max_results]
            # 删除临时key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]

        # 得到商品列表并根据出现的顺序排序
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
            for id in Product.objects.values_list('id', flat=True):
                r.delete(self.get_product_key(id))
