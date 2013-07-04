package ws.donmez.otobur;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.app.ListFragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class DetailsPageFragment extends ListFragment {
    public static final String ARG_PAGE = "page";
    private int mPageNumber;

    private ArrayList<String> stopList;
    private ArrayList<ArrayList<String>> hourList;

    public static DetailsPageFragment create(int pageNumber) {
        DetailsPageFragment fragment = new DetailsPageFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, pageNumber);
        fragment.setArguments(args);
        return fragment;
    }

    public DetailsPageFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setupHourList();
        mPageNumber = getArguments().getInt(ARG_PAGE);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {

        // Inflate the layout containing a title and body text.
        ViewGroup rootView = (ViewGroup) inflater
                .inflate(R.layout.fragment_details_slide_page, container, false);

        TextView tv = (TextView) rootView.findViewById(android.R.id.text1);

        setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                 R.layout.custom_row_layout,
                                                 this.getForwardRoute()));

        setupListView();
        setHeader(tv);

        return rootView;
    }

    public int getPageNumber() {
        return mPageNumber;
    }

    private void setHeader(TextView tv) {
        if (mPageNumber < 2)
            tv.setVisibility(View.GONE);
        else {
            tv.setVisibility(View.VISIBLE);
            tv.setText(stopList.get(mPageNumber - 2));
        }
    }

    private void setupListView() {
        switch (mPageNumber) {
            case 0:
                setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                        R.layout.custom_row_layout,
                                                        this.getForwardRoute()));
                break;
            case 1:
                setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                         R.layout.custom_row_layout,
                                                         this.getBackwardRoute()));
                break;
            default:
                break;
        }

        if (mPageNumber > 1) {
            setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                     R.layout.custom_row_layout,
                                                     this.getHourList(mPageNumber)));
        }
    }

    private ArrayList<String> getForwardRoute() {
        if (MainActivity.currentBus.forward != null)
            return new ArrayList<String>(MainActivity.currentBus.forward);
        else {
            ArrayList<String> dummy = new ArrayList<String>();
            dummy.add(getString(R.string.no_route_data));
            return dummy;
        }
    }

    private ArrayList<String> getBackwardRoute() {
        if (MainActivity.currentBus.backward != null)
            return new ArrayList<String>(MainActivity.currentBus.backward);
        else {
            ArrayList<String> dummy = new ArrayList<String>();
            dummy.add(getString(R.string.no_route_data));
            return dummy;
        }
    }

    private void setupHourList() {
        stopList = new ArrayList<String>();
        hourList = new ArrayList<ArrayList<String>>();
        HashMap<String, ArrayList<String>> busMap =
                new HashMap<String, ArrayList<String>>(MainActivity.currentBus.hours);
        List<String> keys = new ArrayList<String>(busMap.keySet());
        for (String key : keys) {
             hourList.add(new ArrayList<String>(MainActivity.currentBus.hours.get(key)));
             stopList.add(key);
        }
    }

    private ArrayList<String> getHourList(int index) {
        return hourList.get(index-2);
    }
}
