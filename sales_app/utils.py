import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_sales_graph():
  """
  This function will write the graph
  """
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  image_png = buffer.getvalue()
  graph = base64.b64encode(image_png)
  graph = graph.decode('utf-8')
  buffer.close()
  return graph


def get_sales_plot(x_axis_data, y_axis_data):
  """
  This function will generate the plot
  x_axis_data: data for x axis
  y_axis_data: data for y axis
  """
  plt.switch_backend('AGG')
  plt.figure(figsize=(6.5, 5))
  plt.title("Sales of Products")
  plt.bar(x_axis_data, y_axis_data)
  plt.xticks(rotation=45)
  plt.xlabel("Products")
  plt.ylabel("Sales")
  plt.tight_layout()

  graph = get_sales_graph()
  return graph