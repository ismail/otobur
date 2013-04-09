package ws.donmez.burulas;

import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;

public class ForwardStopsActivity extends ListActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setListAdapter(new ArrayAdapter(this,
                                        android.R.layout.simple_list_item_1,
                                        this.getForwardRoute()));
    }

    private ArrayList<String> getForwardRoute() {
        Intent intent = getIntent();

        return intent.getStringArrayListExtra("ForwardStops");
    }
}

