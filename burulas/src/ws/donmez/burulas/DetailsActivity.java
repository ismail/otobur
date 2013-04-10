package ws.donmez.burulas;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;

public class DetailsActivity extends FlingActivity {

    private enum DetailView {
        FORWARD_ROUTE,
        BACKWARD_ROUTE,
        HOUR
    };

    private DetailView currentView;
    private ArrayList<String> backwardRoute;
    private ArrayList<String> forwardRoute;
    private HashMap<String, ArrayList<String>> busMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        currentView = DetailView.FORWARD_ROUTE;
        switchView(currentView);
    }

    @Override
    public void next() {
        switch (currentView) {
            case FORWARD_ROUTE:
                switchView(DetailView.BACKWARD_ROUTE);
                break;
            case BACKWARD_ROUTE:
                switchView(DetailView.HOUR);
                break;
            default:
                break;
        }
    }

    @Override
    public void prev() {
        switch (currentView) {
            case FORWARD_ROUTE:
                finish();
                break;
            case BACKWARD_ROUTE:
                switchView(DetailView.FORWARD_ROUTE);
                break;
            case HOUR:
                switchView(DetailView.BACKWARD_ROUTE);
                break;
            default:
                break;
        }
    }

    private void switchView (DetailView view) {
        switch (view) {
            case FORWARD_ROUTE:
                setListAdapter(new ArrayAdapter<String>(this,
                                R.layout.custom_row_layout,
                                this.getForwardRoute()));
                break;
             case BACKWARD_ROUTE:
                setListAdapter(new ArrayAdapter<String>(this,
                                R.layout.custom_row_layout,
                                this.getBackwardRoute()));
                break;
            case HOUR:
                setListAdapter(new ArrayAdapter<String>(this,
                                R.layout.custom_row_layout,
                                this.getHourList()));
                break;
            default:
                return;

       }

        currentView = view;
    }

    private ArrayList<String> getForwardRoute() {
        if (forwardRoute == null) {
            forwardRoute = new ArrayList<String>(BusViewActivity.currentBus.forward);
            forwardRoute.add(0, ":: Forward Route ::");
        }
        return forwardRoute;
    }

    private ArrayList<String> getBackwardRoute() {
        if (backwardRoute == null) {
            backwardRoute = new ArrayList<String>(BusViewActivity.currentBus.backward);
            backwardRoute.add(0, ":: Backward Route ::");
        }
        return backwardRoute;
    }

    private ArrayList<String> getHourList() {
        if (busMap == null)
            busMap = new HashMap<String, ArrayList<String>>(BusViewActivity.currentBus.hours);
        List<String> keys = new ArrayList<String>(busMap.keySet());
        ArrayList<String> hours = new ArrayList<String>();

        for (String key : keys) {
            hours.add(key);
            hours.addAll((ArrayList<String>) BusViewActivity.currentBus.hours.get(key));
        }

        return hours;
    }
}
