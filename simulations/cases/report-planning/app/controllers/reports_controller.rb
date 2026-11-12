class ReportsController < ApplicationController
  def show
    @workspace = current_user.workspaces.find(session[:workspace_id])
    @report = @workspace.reports.find(params[:id])
    authorize @report
    @rows = params[:report] ? @report.preview(params.require(:report).permit!.to_h) : @report.dataset.rows
  end
end
