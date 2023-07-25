import { useUserStore } from '@/hooks/stores/use-user-store.hook';
import { Product } from '@/models/Product';
import { shoppingCartApi } from '@/services/shoppingCartApi';
import { useQuery } from '@tanstack/react-query';
import { HashLoader } from 'react-spinners';
import { CheckoutDialog } from '@/components/shopping-cart/CheckoutDialog';

export const ShoppingCartPage = () => {
  const user = useUserStore((state) => state.user);
  const { data: shoppingCart, isLoading } = useQuery({
    queryKey: [`shoppingCart-${user!.id}`],
    queryFn: async ({ signal }) => {
      return await shoppingCartApi.getShoppingCart(user!.id, signal!);
    }
  });

  const total = shoppingCart?.reduce((acc, curr) => acc + curr.price, 0) ?? 0;

  return (
    <div>
      <h1 className="mb-5 text-5xl font-bold">Shopping Cart</h1>
      {isLoading && (
        <div className="flex h-48 flex-row items-center justify-center">
          <HashLoader color="#36d7b7" />
        </div>
      )}

      {!isLoading && shoppingCart != undefined && (
        <>
          <h1 className="mb-5 text-4xl font-bold">Items</h1>
          {shoppingCart.map((product: Product) => (
            <p key={product.id}>
              {product.name} - {product.price} $
            </p>
          ))}
          {shoppingCart.length == 0 && (
            <p className="text-lg">Your shopping cart is empty</p>
          )}
          {shoppingCart.length > 0 && (
            <>
              <h2 className="mb-5 text-xl font-bold">Total: {total} $</h2>
              <CheckoutDialog />
            </>
          )}
        </>
      )}
    </div>
  );
};
