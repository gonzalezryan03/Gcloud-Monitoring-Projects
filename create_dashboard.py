from google.cloud import monitoring_dashboard_v1

def create_dashboard(project_id):
    # Dashboard object configs
    dashboard_client = monitoring_dashboard_v1.DashboardsServiceClient()
    dashboard = monitoring_dashboard_v1.types.Dashboard()
    dashboard.display_name = "My App Dashboard"

    dashboard.grid_layout = monitoring_dashboard_v1.types.GridLayout()
    dashboard.grid_layout.columns = 1

    # A simple line chart widget
    chart = monitoring_dashboard_v1.types.Widget()
    chart.title = "Requests Count"
    chart.xy_chart.data_sets.append(
        monitoring_dashboard_v1.types.XyChart.DataSet(
            time_series_query=monitoring_dashboard_v1.types.TimeSeriesQuery(
                time_series_filter=monitoring_dashboard_v1.types.TimeSeriesFilter(
                    filter=f'metric.type = "custom.googleapis.com/myapp/requests_count"'
                )
            ),
            plot_type=monitoring_dashboard_v1.types.XyChart.DataSet.PlotType.LINE
        )
    )
    
    dashboard.grid_layout.widgets.append(chart)

    parent = f"projects/{project_id}"
    created_dashboard = dashboard_client.create_dashboard(
        request={"parent": parent, "dashboard": dashboard}
    )
    print("Created dashboard:", created_dashboard.name)

if __name__ == "__main__":
    PROJECT_ID = "cloud-monitoring-learning"
    create_dashboard(PROJECT_ID)
