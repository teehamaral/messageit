function addProduct() {
  let idProduct = $("#id_product");

  let productTable = $('#product-table');
  let productsBody = document.getElementById('productsBody');

  let rowsAmount = productTable.children('#productsBody').find('tr').length;

  let product = idProduct.val();
  let productName = idProduct.find('option:selected').text();

  var amount = $('#id_amount').val();
  var discount = $('#id_discount').val();

  if (!product) {
    window.alert('Selecione um produto!');
    return
  }

  if (!amount) {
    amount = '1';
  }

  if (!discount) {
    discount = '0,00';
  }

  let row = document.createElement('tr');

  // Product
  let productTd = document.createElement('td');
  let productText = document.createTextNode(productName);

  productTd.appendChild(productText);

  let rowNumber = rowsAmount + 1;

  let productInput = document.createElement('input');
  // productInput.id = rowNumber + '_product';
  // productInput.name = rowNumber + '_product';
  productInput.id = 'product';
  productInput.name = 'product';
  productInput.type = 'hidden';
  productInput.value = product;
  productTd.appendChild(productInput);

  // Amount
  let amountTd = document.createElement('td');
  let amountText = document.createTextNode(amount);

  amountTd.appendChild(amountText);

  let amountInput = document.createElement('input');
  // amountInput.id = rowNumber + '_amount';
  // amountInput.name = rowNumber + '_amount';
  amountInput.id = 'amount';
  amountInput.name = 'amount';
  amountInput.type = 'hidden';
  amountInput.value = amount;
  amountTd.appendChild(amountInput);

  // Discount
  let discountTd = document.createElement('td');
  let discountText = document.createTextNode(discount);

  discountTd.appendChild(discountText);

  let discountInput = document.createElement('input');
  // discountInput.id = rowNumber + '_discount';
  // discountInput.name = rowNumber + '_discount';
  discountInput.id = 'discount';
  discountInput.name = 'discount';
  discountInput.type = 'hidden';
  discountInput.value = discount;
  discountTd.appendChild(discountInput);

  // Action
  let actionTd = document.createElement('td');
  let actionBtn = document.createElement('a');
  actionBtn.href = 'javascript:;';
  actionBtn.onclick = function () {
      removeRow($(this));
  };

  let actionBtnHtml = document.createElement('i');
  actionBtnHtml.className = 'icofont icofont-trash';

  actionBtn.appendChild(actionBtnHtml);
  actionTd.appendChild(actionBtn);

  // Adding tds to row
  row.appendChild(productTd);
  row.appendChild(amountTd);
  row.appendChild(discountTd);
  row.appendChild(actionTd);

  // Adding row to table body
  productsBody.appendChild(row);

  // Reseting form
  let form = $('#product-form');
  console.log(form);
  form[0].reset();
  idProduct.select2("val", "");
  $('#select2-id_product-container').html('---------');
  $('#default-Modal').modal('hide');
}

function removeRow(el) {
  el.parent().parent().remove();
}

function submitForm(event, formType) {
  event.preventDefault();

  let customer = $('#id_customer').val();
  if (!customer) {
    window.alert('Selecione um cliente!');
    return
  }

  let customer_payment_method = $('#id_payment_method').val();
  if (!customer_payment_method) {
    window.alert('Insira o método de pagamento!');
    return
  }

  let customer_payment_condition = $('#id_payment_condition').val();
  if (!customer_payment_condition) {
    window.alert('Insira a condição de pagamento!');
    return
  }

  let productTable = $('#product-table');
  let rowsAmount = productTable.children('#productsBody').find('tr').length;

  // Has products
  if (rowsAmount < 1) {
    window.alert("Produtos não adicionados!");
    return
  }

  $('#form_type').val(formType);
  $('#order-form').submit();

}